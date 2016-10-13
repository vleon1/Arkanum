from formats.helpers import FileStruct

import io


class TerrainHeader(object):

    # Maybe this is a type marker that is always the same?
    # The two values may be one 8bytes value
    # todo: Check that the first value is always 0x3F99999A
    # todo: Check that the second value is always 0x1
    # todo: If the previous are correct, join the parameters and call it "marker"
    unknown1_format = "I"
    unknown2_format = "I"

    sectors_height_format = "Q"
    sectors_width_format = "Q"

    # This is maybe the map type or something, seems to be the same as unknown1 in the prp file
    # todo: validate if always the same as unknown1 in "map.prp"
    unknown3_format = "Q"

    full_format = "<" + unknown1_format + unknown2_format + \
                  sectors_height_format + sectors_width_format + unknown3_format

    parser = FileStruct(full_format)

    def __init__(self, unknown1: int, unknown2: int, sectors_height: int, sectors_width: int, unknown3: int):

        self.unknown1 = unknown1
        self.unknown2 = unknown2

        self.sectors_height = sectors_height
        self.sectors_width = sectors_width

        self.unknown3 = unknown3

    @classmethod
    def read_from(cls, terrain_file_reader: io.BufferedReader) -> "TerrainHeader":

        unknown1, unknown2, sectors_height, sectors_width, unknown3 = cls.parser.unpack_from_file(terrain_file_reader)

        return TerrainHeader(unknown1=unknown1, unknown2=unknown2,
                             sectors_height=sectors_height, sectors_width=sectors_width,
                             unknown3=unknown3)


class Terrain(object):

    # I don't yet know what the entries after the headers hold, but i know that they start with the size
    unknown_entry_length_parser = FileStruct("<I")

    def __init__(self, header: TerrainHeader, number_of_unknown_entries: int):

        self.header = header

        # todo: Assert that the number of entries is always equal to sectors_width
        self.number_of_unknown_entries = number_of_unknown_entries

    @classmethod
    def read(cls, terrain_file_path: str) -> "Terrain":

        number_of_unknown_entries = 0

        with open(terrain_file_path, "rb") as terrain_file:

            terrain_file_reader = io.BufferedReader(terrain_file)

            header = TerrainHeader.read_from(terrain_file_reader)

            while terrain_file_reader.peek():

                number_of_unknown_entries += 1

                unknown_entry_length, = cls.unknown_entry_length_parser.unpack_from_file(terrain_file_reader)
                unknown_entry = terrain_file_reader.read(unknown_entry_length)
                assert len(unknown_entry) == unknown_entry_length

        return Terrain(header=header, number_of_unknown_entries=number_of_unknown_entries)
