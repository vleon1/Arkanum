from formats.helpers import FileStruct


class MapProperties(object):

    # This is the original map type (The type of the tiles the map was created with), here it is saved in 4 bytes
    # And in terrain.tdf it is saved as 8 bytes as well for some reason.
    # This value seems to have little impact (I didn't find yet what uses it, since so far everything i saw used data
    # directly from the sectors descriptors)
    # In 'arcanum1.dat' under 'terrain/forest to snowy plains' there is actually a mismatch with terrain.tdf (That is
    # the only one) so i assume that the value in the here is more important (since the tdf value is the wrong one).
    # The values here fit the values in 'arcanum1.dat' under 'terrain/terrain.mes'
    original_type_format = "I"

    # Different levels of same maps seem to have the same number, the main arcanum map is 1
    # todo: order by this number, and see if it makes sense..
    unknown1_format = "I"

    tiles_height_format = "Q"
    tiles_width_format = "Q"
    full_format = "<" + original_type_format + unknown1_format + tiles_height_format + tiles_width_format

    parser = FileStruct(full_format)

    def __init__(self, file_path: str, original_type: int, unknown1: int, tiles_height: int, tiles_width: int):

        self.file_path = file_path

        self.original_type = original_type
        self.unknown1 = unknown1
        self.tiles_height = tiles_height
        self.tiles_width = tiles_width

    @classmethod
    def read(cls, map_properties_file_path: str) -> "MapProperties":

        with open(map_properties_file_path, "rb") as map_properties_file:

            original_type, unknown1, tiles_height, tiles_width = cls.parser.unpack_from_file(map_properties_file)

            assert not map_properties_file.read()  # todo: remove me

        return MapProperties(file_path=map_properties_file_path,
                             original_type=original_type, unknown1=unknown1,
                             tiles_height=tiles_height, tiles_width=tiles_width)
