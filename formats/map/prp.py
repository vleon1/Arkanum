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

    # This seems to be some kind of a computer stamps, and it seems to only server as informational value.
    # When creating maps with worldEd The whole value can change between computers, on one of my computers the value
    # also change a bit each restart (Only the second byte) on the other the number is always consistent.
    stamp_format = "I"

    tile_rows_format = "Q"
    tile_cols_format = "Q"
    full_format = "<" + original_type_format + stamp_format + tile_rows_format + tile_cols_format

    parser = FileStruct(full_format)

    def __init__(self, file_path: str, original_type: int, stamp: int, tile_rows: int, tile_cols: int):

        self.file_path = file_path

        self.original_type = original_type
        self.stamp = stamp
        self.tile_rows = tile_rows
        self.tile_cols = tile_cols

    @classmethod
    def read(cls, map_properties_file_path: str) -> "MapProperties":

        with open(map_properties_file_path, "rb") as map_properties_file:

            original_type, stamp, tile_rows, tile_cols = cls.parser.unpack_from_file(map_properties_file)

        return MapProperties(file_path=map_properties_file_path,
                             original_type=original_type, stamp=stamp,
                             tile_rows=tile_rows, tile_cols=tile_cols)
