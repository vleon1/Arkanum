from formats.helpers import FileStruct

from typing import List
import io


class TerrainHeader(object):

    class DescriptorTypeHeader(object):

        no_descriptors = 0x3F8CCCCD
        simple_or_complex_descriptors = 0x3F99999A

    class DescriptorsType(object):

        no_descriptors = "no descriptors"
        simple_descriptors = "simple descriptors"
        complex_descriptors = "complex descriptors"

        descriptors_header_to_type = {
            0x03F8CCCCD : no_descriptors,
            0x03F99999A: simple_descriptors,
            0x13F99999A: complex_descriptors,
        }

    # It might be more complex than that, but from 100% of the data i tested it was acting according to the
    # DescriptorTypeHeader definition.
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
    def read_from(cls, terrain_file_reader: io.FileIO) -> "TerrainHeader":

        descriptors_header, sectors_height, sectors_width, original_type = \
            cls.parser.unpack_from_file(terrain_file_reader)

        return TerrainHeader(descriptors_header=descriptors_header,
                             sectors_height=sectors_height, sectors_width=sectors_width,
                             original_type=original_type)


# todo: figure this out...
class Descriptor(object):

    def __init__(self, data: bytes):
        self.data = data

    # todo: remove or update me
    def __repr__(self):
        return str(len(self.data))


class Terrain(object):

    simple_descriptor_parser = FileStruct("<2s")
    complex_descriptor_length_parser = FileStruct("<I")

    def __init__(self, file_path: str, header: TerrainHeader, descriptors: List[Descriptor]):

        self.file_path = file_path

        self.header = header

        self.descriptors = descriptors

    @classmethod
    def read(cls, terrain_file_path: str) -> "Terrain":

        descriptors = []  # type: List[Descriptor]

        with open(terrain_file_path, "rb") as terrain_file:

            header = TerrainHeader.read_from(terrain_file)

            if header.descriptors_type == TerrainHeader.DescriptorsType.simple_descriptors:

                for _ in range(header.sectors_height * header.sectors_width):

                    descriptor_data, = cls.simple_descriptor_parser.unpack_from_file(terrain_file)
                    descriptor = Descriptor(data=descriptor_data)
                    descriptors.append(descriptor)

            elif header.descriptors_type == TerrainHeader.DescriptorsType.complex_descriptors:

                for _ in range(header.sectors_width):

                    descriptor_length, = cls.complex_descriptor_length_parser.unpack_from_file(terrain_file)

                    descriptor_data = terrain_file.read(descriptor_length)

                    assert len(descriptor_data) == descriptor_length   # todo: remove me
                    assert descriptor_data[:2] == b"\x78\xDA"  # todo: remove me

                    descriptor = Descriptor(data=descriptor_data)

                    descriptors.append(descriptor)

                assert not terrain_file.read()  # todo: remove me

        return Terrain(file_path=terrain_file_path, header=header, descriptors=descriptors)
