from formats.helpers import FileStruct


class MapProperties(object):

    # This might be map type, but probably not.
    # The value seems to be the same as an 8bytes unknown in the terrain.tdf file
    # I checked and at least the first few arcanum maps (including the main one) have this value set as 2
    # todo: Validate that this unknowns is always the same value as the tdf unknown
    # todo: group by this number, and see if its terrain type or something else
    unknown1_format = "I"

    # Different levels of same maps seem to have the same number, the main arcanum map is 1
    # todo: order by this number, and see if it makes sense..
    unknown2_format = "I"

    tiles_height_format = "Q"  # todo: Need to check if its always 64 * sectors_height
    tiles_width_format = "Q"  # todo: Need to check if its always 64 * sectors_width
    full_format = "<" + unknown1_format + unknown2_format + tiles_height_format + tiles_width_format

    parser = FileStruct(full_format)

    def __init__(self, unknown1: int, unknown2: int, tiles_height: int, tiles_width: int):

        self.unknown1 = unknown1
        self.unknown2 = unknown2
        self.tiles_height = tiles_height
        self.tiles_width = tiles_width

    @classmethod
    def read(cls, map_properties_file_path: str) -> "MapProperties":

        with open(map_properties_file_path, "rb") as map_properties_file:

            unknown1, unknown2, tiles_height, tiles_width = cls.parser.unpack_from_file(map_properties_file)

            assert not map_properties_file.read()  # todo: remove me

        return MapProperties(unknown1=unknown1, unknown2=unknown2, tiles_height=tiles_height, tiles_width=tiles_width)
