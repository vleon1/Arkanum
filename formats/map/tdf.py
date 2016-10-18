from formats.helpers import FileStruct

import zlib
import io

from typing import Dict, Tuple

import numpy


class TerrainHeader(object):

    class DescriptorsType(object):

        no_descriptors = "no descriptors"
        simple_descriptors = "simple descriptors"
        compressed_descriptors = "compressed descriptors"

        descriptors_header_to_type = {
            0x03F8CCCCD: no_descriptors,
            0x03F99999A: simple_descriptors,
            0x13F99999A: compressed_descriptors,
        }

        descriptors_type_to_header = {t: h for h, t in descriptors_header_to_type.items()}

    # It might be more complex than that, but from 100% of the data i tested it was acting according to the
    # DescriptorsType definition.
    # Also the only file that has no descriptors is in 'arcanum1.dat' under 'terrain/tropical mountains/terrain.tdf'
    descriptors_header_format = "Q"

    sectors_height_format = "Q"
    sectors_width_format = "Q"

    # This is the original map type (The type of the tiles the map was created with), here it is saved in 8 bytes
    # And in map.prp it is saved as 4 bytes as well for some reason.
    # This value seems to have little impact (I didn't find yet what uses it, since so far everything i saw used data
    # directly from the sectors descriptors)
    # In 'arcanum1.dat' under 'terrain/forest to snowy plains' there is actually a mismatch with map.prp (That is
    # the only one) so i assume that the value in the prp file is more important (since the tdf value is the wrong one).
    # The values here fit the values in 'arcanum1.dat' under 'terrain/terrain.mes'
    original_type_format = "Q"

    full_format = "<" + descriptors_header_format + sectors_height_format + sectors_width_format + original_type_format

    parser = FileStruct(full_format)

    def __init__(self, descriptors_header: int, sectors_height: int, sectors_width: int, original_type: int):

        self.descriptors_type = self.DescriptorsType.descriptors_header_to_type[descriptors_header]

        self.sectors_height = sectors_height
        self.sectors_width = sectors_width

        self.original_type = original_type

    @classmethod
    def read_from(cls, terrain_file: io.FileIO) -> "TerrainHeader":

        descriptors_header, sectors_height, sectors_width, original_type = \
            cls.parser.unpack_from_file(terrain_file)

        return TerrainHeader(descriptors_header=descriptors_header,
                             sectors_height=sectors_height, sectors_width=sectors_width,
                             original_type=original_type)

    def write_to(self, terrain_file: io.FileIO) -> None:

        if self.descriptors_type == self.DescriptorsType.no_descriptors:
            output_descriptors_type = self.DescriptorsType.no_descriptors
        else:
            output_descriptors_type = self.DescriptorsType.simple_descriptors

        descriptors_header = self.DescriptorsType.descriptors_type_to_header[output_descriptors_type]

        header_data = self.parser.pack(descriptors_header, self.sectors_height, self.sectors_width, self.original_type)

        terrain_file.write(header_data)


class Descriptor(object):

    # I don't know yet if the data is separated or together, and what it means.*[]
    # todo: figure this out...
    unknown1_format = "B"
    unknown2_format = "B"

    full_format = "<" + unknown1_format + unknown2_format

    parser = FileStruct(full_format)

    def __init__(self, unknown1: int, unknown2: int):

        self.unknown1 = unknown1
        self.unknown2 = unknown2

    @classmethod
    def read_from(cls, terrain_file: io.BytesIO) -> "Descriptor":

        unknown1, unknown2 = cls.parser.unpack_from_file(terrain_file)

        return Descriptor(unknown1=unknown1, unknown2=unknown2)

    def write_to(self, terrain_file: io.FileIO) -> None:

        descriptor_data = self.parser.pack(self.unknown1, self.unknown2)

        terrain_file.write(descriptor_data)


class Terrain(object):

    descriptor_parser = FileStruct("<2s")
    compressed_descriptors_length_parser = FileStruct("<I")

    def __init__(self, file_path: str, header: TerrainHeader, descriptors: Dict[Tuple[int, int], Descriptor]):

        self.file_path = file_path

        self.header = header

        self.descriptors = descriptors

    @classmethod
    def read(cls, terrain_file_path: str) -> "Terrain":

        with open(terrain_file_path, "rb") as terrain_file:

            header = TerrainHeader.read_from(terrain_file)

            if header.descriptors_type == TerrainHeader.DescriptorsType.no_descriptors:

                descriptors = None

            else:

                if header.descriptors_type == TerrainHeader.DescriptorsType.simple_descriptors:

                    descriptors_raw = io.BytesIO(terrain_file.read())

                else:

                    descriptors_raw = io.BytesIO()

                    for _ in range(header.sectors_width):
                        descriptors_raw_data_length, = cls.compressed_descriptors_length_parser.unpack_from_file(
                            terrain_file)

                        descriptors_raw_data = terrain_file.read(descriptors_raw_data_length)

                        descriptors_data = zlib.decompress(descriptors_raw_data)

                        descriptors_raw.write(descriptors_data)

                    descriptors_raw.seek(0, io.SEEK_SET)

                shape = (header.sectors_height, header.sectors_width)
                descriptors = numpy.empty(shape=shape, dtype=object)  # type: Dict[Tuple[int, int], Descriptor]

                for x in range(header.sectors_height):
                    for y in range(header.sectors_width):
                        descriptors[x, y] = Descriptor.read_from(descriptors_raw)

        return Terrain(file_path=terrain_file_path, header=header, descriptors=descriptors)

    def write(self, terrain_file_path: str) -> None:

        with open(terrain_file_path, "wb") as terrain_file:

            self.header.write_to(terrain_file)

            for x in range(self.header.sectors_height):
                for y in range(self.header.sectors_width):
                    self.descriptors[x, y].write_to(terrain_file)
