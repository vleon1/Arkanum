from formats.helpers import FileStruct

import zlib
import io

from typing import Dict, Tuple, Union, Iterator

import numpy


# Used for type checking only
NumpyMatrix = Union[Dict[Tuple[int, int], int], numpy.ndarray, None]


"""
An ordered tuple of terrains, the index fits the number used to describe that terrain type

The indexes and names where taken from 'arcanum1.dat' under 'terrain/terrain.mes'
"""
terrain_types = ("green grasslands", "swamps", "water", "plains", "forest", "desert island", "void plains",
                 "broad leaf forest", "desert", "mountains", "elven forest", "deforested", "snowy plains",
                 "tropical jungle", "void mountains", "scorched earth", "desert mountains", "snowy mountains",
                 "tropical mountains")


class TerrainHeader(object):

    class DescriptorsType(object):

        no_descriptors = 0x03F8CCCCD
        simple_descriptors = 0x03F99999A
        compressed_descriptors = 0x13F99999A

    # It might be more complex than that, but from 100% of the data i tested it was acting according to the
    # DescriptorsType definition.
    # Also the only file that has no descriptors is in 'arcanum1.dat' under 'terrain/tropical mountains/terrain.tdf'
    descriptors_header_format = "Q"

    sector_rows_format = "Q"
    sector_cols_format = "Q"

    # This is the original map type (The type of the tiles the map was created with), here it is saved in 8 bytes
    # And in map.prp it is saved as 4 bytes as well for some reason.
    # This value seems to have little impact (I didn't find yet what uses it, since so far everything i saw used data
    # directly from the sectors descriptors)
    # In 'arcanum1.dat' under 'terrain/forest to snowy plains' there is actually a mismatch with map.prp (That is
    # the only one) so i assume that the value in the prp file is more important (since the tdf value is the wrong one).
    # The values here fit the values in 'arcanum1.dat' under 'terrain/terrain.mes'
    original_type_format = "Q"

    full_format = "<" + descriptors_header_format + sector_rows_format + sector_cols_format + original_type_format

    parser = FileStruct(full_format)

    def __init__(self, descriptors_type: int, sector_rows: int, sector_cols: int, original_type: int):

        self.descriptors_type = descriptors_type

        self.sector_rows = sector_rows
        self.sector_cols = sector_cols

        self.original_type = original_type

    @classmethod
    def read_from(cls, terrain_file: io.FileIO) -> "TerrainHeader":

        descriptors_header, sector_rows, sector_cols, original_type = \
            cls.parser.unpack_from_file(terrain_file)

        return TerrainHeader(descriptors_type=descriptors_header,
                             sector_rows=sector_rows, sector_cols=sector_cols,
                             original_type=original_type)

    def write_to(self, terrain_file: io.FileIO) -> None:

        # todo: save compressed data as well in some cases
        if self.descriptors_type == self.DescriptorsType.no_descriptors:
            descriptors_type = self.DescriptorsType.no_descriptors
        else:
            descriptors_type = self.DescriptorsType.simple_descriptors

        header_data = self.parser.pack(descriptors_type, self.sector_rows, self.sector_cols, self.original_type)

        terrain_file.write(header_data)


class Descriptor(object):

    # I don't know yet if the data is separated or together, and what it means.*[]
    # todo: validate
    index_and_terrain_type_format = "H"

    full_format = "<" + index_and_terrain_type_format

    parser = FileStruct(full_format)

    def __init__(self, index_and_terrain_type: int):

        self.index_and_terrain_type = index_and_terrain_type

    @property
    def index(self) -> int:
        return self.index_and_terrain_type & 0b111111

    @property
    def to_terrain_index(self) -> int:
        return (self.index_and_terrain_type >> 6) & 0b11111

    @property
    def from_terrain_index(self) -> int:
        return (self.index_and_terrain_type >> 11) & 0b11111

    @property
    def to_terrain(self) -> str:
        return terrain_types[self.to_terrain_index]

    @property
    def from_terrain(self) -> str:
        return terrain_types[self.from_terrain_index]

    def write_to(self, terrain_file: io.FileIO) -> None:

        descriptor_data = self.parser.pack(self.index_and_terrain_type)

        terrain_file.write(descriptor_data)


class Terrain(object):

    compressed_descriptors_length_parser = FileStruct("<I")
    raw_descriptor_type = numpy.uint16

    def __init__(self, file_path: str, header: TerrainHeader, raw_descriptors: NumpyMatrix):

        self.file_path = file_path

        self.header = header

        self.raw_descriptors = raw_descriptors

    @property
    def cols(self) -> int:
        return self.header.sector_cols

    @property
    def rows(self) -> int:
        return self.header.sector_rows

    @property
    def has_descriptors(self) -> bool:
        return self.header.descriptors_type != TerrainHeader.DescriptorsType.no_descriptors

    @property
    def has_compressed_descriptors(self) -> bool:
        return self.header.descriptors_type == TerrainHeader.DescriptorsType.compressed_descriptors

    def __getitem__(self, row_col: Tuple[int, int]) -> Descriptor:
        """ Returns a descriptor of the requested sector """

        raw_descriptor = self.raw_descriptors[row_col]

        return Descriptor(raw_descriptor)

    @classmethod
    def read(cls, terrain_file_path: str) -> "Terrain":

        with open(terrain_file_path, "rb") as terrain_file:

            header = TerrainHeader.read_from(terrain_file)

            if header.descriptors_type == TerrainHeader.DescriptorsType.no_descriptors:

                return Terrain(file_path=terrain_file_path, header=header, raw_descriptors=None)

            if header.descriptors_type == TerrainHeader.DescriptorsType.simple_descriptors:

                raw_descriptors = numpy.fromfile(file=terrain_file, dtype=cls.raw_descriptor_type)  # type: NumpyMatrix

                shape = (header.sector_cols, header.sector_rows)
                raw_descriptors = raw_descriptors.reshape(shape).transpose()  # type: NumpyMatrix

                return Terrain(file_path=terrain_file_path, header=header, raw_descriptors=raw_descriptors)

            elif header.descriptors_type == TerrainHeader.DescriptorsType.compressed_descriptors:

                uncompressed_descriptor_columns_iterator = cls._yield_uncompressed_descriptor_columns(
                    terrain_file=terrain_file, header=header)

                raw_descriptors = numpy.stack(uncompressed_descriptor_columns_iterator).transpose()  # type: NumpyMatrix

                return Terrain(file_path=terrain_file_path, header=header, raw_descriptors=raw_descriptors)

            else:

                raise Exception("Bad descriptors header!")

    def write(self, terrain_file_path: str) -> None:

        with open(terrain_file_path, "wb") as terrain_file:

            self.header.write_to(terrain_file)

            if not self.has_descriptors:
                return

            for col in range(self.cols):
                for row in range(self.rows):
                    self[row, col].write_to(terrain_file)

    @classmethod
    def _yield_uncompressed_descriptor_columns(cls,
                                               terrain_file: io.FileIO,
                                               header: TerrainHeader) -> Iterator(numpy.ndarray):

        for _ in range(header.sector_cols):

            col_compressed_data_length, = cls.compressed_descriptors_length_parser.unpack_from_file(terrain_file)

            col_compressed_data = terrain_file.read(col_compressed_data_length)

            col_data = zlib.decompress(col_compressed_data)

            yield numpy.frombuffer(buffer=col_data, dtype=cls.raw_descriptor_type)
