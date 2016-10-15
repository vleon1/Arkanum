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

    # It might be more complex than that, but from 100% of the data i tested it was acting according to th
    # DescriptorTypeHeader definition.
    # Also the only file that has no descriptors (and thus has the unique no_descriptors type header) is in arcanum1.dat
    # under 'terrain/tropical mountains/terrain.tdf'
    descriptors_type_header_format = "I"

    # It might be more complex than that, but from 100% of the data i tested it was acting like a boolean
    # 1 for complex descriptors, zero if not.
    has_complex_descriptors_format = "I"

    sectors_height_format = "Q"
    sectors_width_format = "Q"

    # This is maybe the map type or something, seems to be the same as unknown1 in the prp file
    # todo: validate if always the same as unknown1 in "map.prp"
    unknown3_format = "Q"

    full_format = "<" + descriptors_type_header_format + has_complex_descriptors_format + \
                  sectors_height_format + sectors_width_format + unknown3_format

    parser = FileStruct(full_format)

    def __init__(self, descriptors_type_header: int, has_complex_descriptors: int,
                 sectors_height: int, sectors_width: int, unknown3: int):

        bad_descriptors_info = False
        if descriptors_type_header == self.DescriptorTypeHeader.simple_or_complex_descriptors:
            if has_complex_descriptors == 1:
                self.descriptors_type = self.DescriptorsType.complex_descriptors
            elif has_complex_descriptors == 0:
                self.descriptors_type = self.DescriptorsType.simple_descriptors
            else:
                bad_descriptors_info = True
        elif descriptors_type_header == self.DescriptorTypeHeader.no_descriptors and has_complex_descriptors == 0:
            self.descriptors_type = self.DescriptorsType.no_descriptors
        else:
            bad_descriptors_info = True

        if bad_descriptors_info:
            raise Exception("Unexpected descriptors_type_header %X or has_complex_descriptors value %d" %
                            (descriptors_type_header, has_complex_descriptors))

        self.sectors_height = sectors_height
        self.sectors_width = sectors_width

        self.unknown3 = unknown3

    @classmethod
    def read_from(cls, terrain_file_reader: io.FileIO) -> "TerrainHeader":

        descriptors_type_header, has_complex_descriptors, sectors_height, sectors_width, unknown3 = \
            cls.parser.unpack_from_file(terrain_file_reader)

        return TerrainHeader(descriptors_type_header=descriptors_type_header,
                             has_complex_descriptors=has_complex_descriptors,
                             sectors_height=sectors_height, sectors_width=sectors_width,
                             unknown3=unknown3)


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

    def __init__(self, header: TerrainHeader, descriptors: List[Descriptor]):

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

                    descriptor = Descriptor(data=descriptor_data)

                    descriptors.append(descriptor)

                assert not terrain_file.read()  # todo: remove me

        return Terrain(header=header, descriptors=descriptors)
