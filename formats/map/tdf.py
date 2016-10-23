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
terrain_index_to_name = (
    "green grasslands",    # 00
    "swamps",              # 01
    "water",               # 02
    "plains",              # 03
    "forest",              # 04
    "desert island",       # 05
    "void plains",         # 06
    "broad leaf forest",   # 07
    "desert",              # 08
    "mountains",           # 09
    "elven forest",        # 10
    "deforested",          # 11
    "snowy plains",        # 12
    "tropical jungle",     # 13
    "void mountains",      # 14
    "scorched earth",      # 15
    "desert mountains",    # 16
    "snowy mountains",     # 17
    "tropical mountains",  # 18
)


class TerrainHeader(object):

    class SectorPointersType(object):

        no_pointers = 0x03F8CCCCD
        simple_pointers = 0x03F99999A
        compressed_pointers = 0x13F99999A

    """
    It might be more complex than that, but from 100% of the data i tested it was acting according to the
    SectorPointersType definition.
    Also the only file that has no pointers is in 'arcanum1.dat' under 'terrain/tropical mountains/terrain.tdf'
    """
    sector_pointers_type_format = "Q"

    sector_rows_format = "Q"
    sector_cols_format = "Q"

    """
    This is the original map type (The type of the tiles the map was created with), here it is saved in 8 bytes
    And in map.prp it is saved as 4 bytes as well for some reason.
    This value seems to have little impact (I didn't find yet what uses it, since so far everything i saw used data
    directly from the sectors pointers)
    In 'arcanum1.dat' under 'terrain/forest to snowy plains' there is actually a mismatch with map.prp (That is
    the only one) so i assume that the value in the prp file is more important (since the tdf value is the wrong one).
    The values here fit the values in 'arcanum1.dat' under 'terrain/terrain.mes'
    """
    original_type_format = "Q"

    full_format = "<" + sector_pointers_type_format + sector_rows_format + sector_cols_format + original_type_format

    parser = FileStruct(full_format)

    def __init__(self, sector_pointers_type: int, sector_rows: int, sector_cols: int, original_type: int):

        self.sector_pointers_type = sector_pointers_type

        self.sector_rows = sector_rows
        self.sector_cols = sector_cols

        self.original_type = original_type

    @classmethod
    def read_from(cls, terrain_file: io.FileIO) -> "TerrainHeader":

        sector_pointers_type, sector_rows, sector_cols, original_type = cls.parser.unpack_from_file(terrain_file)

        return TerrainHeader(sector_pointers_type=sector_pointers_type,
                             sector_rows=sector_rows, sector_cols=sector_cols,
                             original_type=original_type)

    def write_to(self, terrain_file: io.FileIO) -> None:

        # todo: save compressed data as well in some cases
        if self.sector_pointers_type == self.SectorPointersType.no_pointers:
            sector_pointers_type = self.SectorPointersType.no_pointers
        else:
            sector_pointers_type = self.SectorPointersType.simple_pointers

        header_data = self.parser.pack(sector_pointers_type, self.sector_rows, self.sector_cols, self.original_type)

        terrain_file.write(header_data)


class SectorPointer(object):

    class MixedTerrainCoordinates(object):
        """
        When dealing with mixed terrains the indexes are very complex, i think the binary meaning of the numbers
        has a pattern but its not that important or interesting for me to figure out.
        So instead we have this helper class that holds coordinates an a boolean that indicates whether to use the
        map named after the from to transition (for example "green grasslands to water") or use the inverse transition
        for example "water to green grasslands").
        """

        def __init__(self, row: int, col: int, is_inverse_map: bool):
            self.row = row
            self.col = col
            self.is_inverse_map = is_inverse_map

    """ Used to translate the mixed_terrain_index property to a descriptor that helps getting the actual sector """
    # todo: Figure out why number 5 in "green grasslands to water" is different from "water to green grasslands"
    mixed_index_to_coordinates = (
        None,                                                         # 00
        MixedTerrainCoordinates(row=1, col=0, is_inverse_map=False),  # 01
        MixedTerrainCoordinates(row=1, col=2, is_inverse_map=False),  # 02
        MixedTerrainCoordinates(row=1, col=1, is_inverse_map=False),  # 03
        MixedTerrainCoordinates(row=3, col=2, is_inverse_map=False),  # 04
        MixedTerrainCoordinates(row=0, col=0, is_inverse_map=False),  # 05
        MixedTerrainCoordinates(row=2, col=2, is_inverse_map=False),  # 06
        MixedTerrainCoordinates(row=3, col=0, is_inverse_map=True),   # 07
        MixedTerrainCoordinates(row=3, col=0, is_inverse_map=False),  # 08
        MixedTerrainCoordinates(row=2, col=0, is_inverse_map=False),  # 09
        MixedTerrainCoordinates(row=0, col=0, is_inverse_map=True),   # 10
        MixedTerrainCoordinates(row=3, col=2, is_inverse_map=True),   # 11
        MixedTerrainCoordinates(row=3, col=1, is_inverse_map=False),  # 12
        MixedTerrainCoordinates(row=1, col=2, is_inverse_map=True),   # 13
        MixedTerrainCoordinates(row=1, col=0, is_inverse_map=True),   # 14
    )

    pointer_data_format = "H"

    full_format = "<" + pointer_data_format

    # For now only used for writing, parsing is done in bulks for efficiency reasons
    # todo: remove me
    parser = FileStruct(full_format)

    def __init__(self, pointer_data: int):

        self.pointer_data = pointer_data

    @property
    def index(self) -> int:
        return self.pointer_data & 0b11

    @property
    def mixed_terrain_index(self) -> int:
        """
        This index is translated to coordinates with the 'mixed_index_to_coordinates' tuple.
        """
        return (self.pointer_data >> 2) & 0b1111

    @property
    def to_terrain_index(self) -> int:
        return (self.pointer_data >> 6) & 0b11111

    @property
    def from_terrain_index(self) -> int:
        return (self.pointer_data >> 11) & 0b11111

    def to_terrain_name(self) -> str:
        return terrain_index_to_name[self.to_terrain_index]

    def from_terrain_name(self) -> str:
        return terrain_index_to_name[self.from_terrain_index]

    def write_to(self, terrain_file: io.FileIO) -> None:
        # todo: remove and write in bulks

        sector_pointer_data = self.parser.pack(self.pointer_data)

        terrain_file.write(sector_pointer_data)


class Terrain(object):

    compressed_sector_pointers_length_parser = FileStruct("<I")
    raw_sector_pointer_type = numpy.uint16

    def __init__(self, file_path: str, header: TerrainHeader, raw_sector_pointers: NumpyMatrix):

        self.file_path = file_path

        self.header = header

        self.raw_sector_pointers = raw_sector_pointers

    @property
    def cols(self) -> int:
        return self.header.sector_cols

    @property
    def rows(self) -> int:
        return self.header.sector_rows

    @property
    def has_sector_pointers(self) -> bool:
        return self.header.sector_pointers_type != TerrainHeader.SectorPointersType.no_pointers

    @property
    def has_compressed_sector_pointers(self) -> bool:
        return self.header.sector_pointers_type == TerrainHeader.SectorPointersType.compressed_pointers

    def __getitem__(self, row_col: Tuple[int, int]) -> SectorPointer:
        """ Returns a pointer of the requested sector """

        raw_sector_pointer = self.raw_sector_pointers[row_col]

        return SectorPointer(raw_sector_pointer)

    @classmethod
    def read(cls, terrain_file_path: str) -> "Terrain":

        with open(terrain_file_path, "rb") as terrain_file:

            header = TerrainHeader.read_from(terrain_file)

            if header.sector_pointers_type == TerrainHeader.SectorPointersType.no_pointers:

                return Terrain(file_path=terrain_file_path, header=header, raw_sector_pointers=None)

            if header.sector_pointers_type == TerrainHeader.SectorPointersType.simple_pointers:

                raw_pointers = numpy.fromfile(file=terrain_file, dtype=cls.raw_sector_pointer_type)  # type: NumpyMatrix

                shape = (header.sector_cols, header.sector_rows)
                raw_pointers = raw_pointers.reshape(shape).transpose()  # type: NumpyMatrix

                return Terrain(file_path=terrain_file_path, header=header, raw_sector_pointers=raw_pointers)

            elif header.sector_pointers_type == TerrainHeader.SectorPointersType.compressed_pointers:

                columns_iterator = cls._yield_uncompressed_sector_pointers_columns(
                    terrain_file=terrain_file, header=header)

                raw_pointers = numpy.stack(columns_iterator).transpose()  # type: NumpyMatrix

                return Terrain(file_path=terrain_file_path, header=header, raw_sector_pointers=raw_pointers)

            else:

                raise Exception("Bad pointers type header!")

    def write(self, terrain_file_path: str) -> None:

        with open(terrain_file_path, "wb") as terrain_file:

            self.header.write_to(terrain_file)

            if not self.has_sector_pointers:
                return

            for col in range(self.cols):
                for row in range(self.rows):
                    self[row, col].write_to(terrain_file)

    @classmethod
    def _yield_uncompressed_sector_pointers_columns(cls,
                                                    terrain_file: io.FileIO,
                                                    header: TerrainHeader) -> Iterator(numpy.ndarray):

        for _ in range(header.sector_cols):

            col_compressed_data_length, = cls.compressed_sector_pointers_length_parser.unpack_from_file(terrain_file)

            col_compressed_data = terrain_file.read(col_compressed_data_length)

            col_data = zlib.decompress(col_compressed_data)

            yield numpy.frombuffer(buffer=col_data, dtype=cls.raw_sector_pointer_type)
