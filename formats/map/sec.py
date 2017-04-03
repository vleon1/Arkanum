from formats.helpers import FileStruct

import io

from typing import List, Any


class SectorLights(object):
    """
    Binary file format:
    - Light count (4 bytes)
    - Light (48 bytes) * Light count
    """
    count_format = "<I"
    raw_format = "48s"


    def __init__(self, raw_lights: List[Any]):

        self.raw_lights = raw_lights

    def __len__(self) -> int:
        return len(self.raw_lights)

    def __getitem__(self, index: int) -> int:
        return self.raw_lights[index]

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorLights":

        count, = FileStruct.cached_unpack_from_file(cls.count_format, sector_file)

        if (count > 0):
            fmt = "<" + cls.raw_format * count
            raw_lights = FileStruct.cached_unpack_from_file(fmt, sector_file)
        else:
            raw_lights = []

        return SectorLights(raw_lights)

    def write_to(self, sector_file: io.FileIO) -> None:

        count = len(self.raw_lights)
        FileStruct.cached_pack_to_file(self.count_format, sector_file, count)

        if (count > 0):
            fmt = "<" + self.raw_format * count
            FileStruct.cached_pack_to_file(fmt, sector_file, self.raw_lights)


class SectorTiles(object):
    """
    Binary file format:
    - Tile (4 bytes) * 4096

    Binary file format per tile (old notes: might be little or big endian):
    First byte:
    - Flipped (1 bit)
    - Unknown (4 bits)
    - Flippable (2 bits)
    Second byte:
    - Outdoor (1 bit)
    - Variant (3 bits) (tile file name ending with a, b, ..., or h)
    - Rotation (4 bits)
    Third / Fourth byte:
    - Some index (6 bits)  # Probably indicates the art file prefix to use.
    - Some index (6 bits)  # In my notes its stated to always be the same as the former, 
                           # but its probably the other terrain in a transition.
    - Unknown (4 bits)
    """
    raw_tiles_format = "<4096I"
    raw_tiles_parser = FileStruct(raw_tiles_format)

    def __len__(self) -> int:
        return len(self.raw_tiles)

    def __getitem__(self, index: int) -> int:
        return self.raw_tiles[index]

    def __init__(self, raw_tiles: List[Any]):

        self.raw_tiles = raw_tiles

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorTiles":

        raw_tiles = cls.raw_tiles_parser.unpack_from_file(sector_file)

        return SectorTiles(raw_tiles)

    def write_to(self, sector_file: io.FileIO) -> None:

        raw_tiles_data = self.raw_tiles_parser.pack_to_file(self.raw_tiles, sector_file)


class SectorRoofs(object):
    """
    Binary file format:
    - Roof (4 bytes) * 256
    """

    roofs_type_format = "<I"
    raw_roofs_format = "<256I"

    raw_roofs_parser = FileStruct(raw_roofs_format)

    def __init__(self, type: int, raw_roofs: List[Any]):

        self.type = type
        self.raw_roofs = raw_roofs

    def __len__(self) -> int:

        return len(self.raw_roofs)

    def __getitem__(self, index: int) -> int:

        return self.raw_roofs[index]

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorRoofs":

        roofs_type, = FileStruct.cached_unpack_from_file(cls.roofs_type_format, sector_file)

        if roofs_type == 0:
            raw_roofs = cls.raw_roofs_parser.unpack_from_file(sector_file)
        else:
            raw_roofs = []
        return SectorRoofs(type=roofs_type, raw_roofs=raw_roofs)

    def write_to(self, sector_file: io.FileIO) -> None:

        FileStruct.cached_pack()

        raw_tiles_data = FileStruct.cached_pack_to_file(self.raw_roofs_format, sector_file, self.raw_roofs)


class SectorScripts(object):
    """
    Binary file format:
    - Tile scripts count (4 bytes)
    - Tile script (24 bytes) * count

    Binary file format per tile script:
    - ? (4 bytes)
    - Index of tile in sector (2 bytes)
    - ? (2 bytes)
    - Flags (3 bytes)
    - ? (1 byte) 
    - Counters (4 bytes)
    - Script ID (4 bytes)
    - ? (4 bytes)
    """
    count_format = "<I"
    raw_format = "24s"

    def __init__(self, raw_scripts: List[Any]):

        self.raw_scripts = raw_scripts

    def __len__(self) -> int:

        return len(self.raw_scripts)

    def __getitem__(self, index: int) -> int:

        return self.raw_scripts[index]

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorScripts":

        count, = FileStruct.cached_unpack_from_file(cls.count_format, sector_file)
        if (count > 0):
            fmt = "<" + cls.raw_format * count
            raw_scripts = FileStruct.cached_unpack_from_file(fmt, sector_file)
        else:
            raw_scripts = []

        return SectorScripts(raw_scripts=raw_scripts)

    def write_to(self, sector_file: io.FileIO) -> None:

        count = len(self.raw_scripts)
        count_data = FileStruct.cached_pack_to_file(self.count_format, sector_file, count)

        if (count > 0):
            fmt = "<" + self.raw_format * count
            raw_data = FileStruct.cached_pack_to_file(fmt, sector_file, self.raw_scripts)

class SectorBlockades(object):
    """
    Binary file format:
    - Blocked (1 bit) * 4096
    """
    raw_blockades_format = "<512B"
    raw_blockades_parser = FileStruct(raw_blockades_format)

    def __init__(self, raw_blockades: List[Any]):

        self.raw_blockades = raw_blockades

    def __len__(self) -> int:

        return len(self.raw_blockades)

    def __getitem__(self, index: int) -> int:

        return self.raw_blockades[index]

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorBlockades":

        raw_blockades = cls.raw_blockades_parser.unpack_from_file(sector_file)
        
        return SectorBlockades(raw_blockades=raw_blockades)

    def write_to(self, sector_file: io.FileIO) -> None:

        self.raw_blockades_parser.pack_to_file(sector_file, self.raw_blockades)



class Sector(object):
    """
    Binary file format (everything unsigned unless explicitly mentioned): 
    - Light count (4 bytes)
    - List of lights (n * 48 bytes)
    - Array of 4096 tiles (64 * 64 * 4 bytes)
    - Roof list type (4 bytes)
        If roof list type == 0
        - Array of 256 roofs (16 * 16 * 4 bytes)
    - ? (4 bytes)
    - Script tile count (4 bytes)
        # List of tile scripts (n * 24 bytes)
    - ? (4 bytes)
    - ? (4 bytes)
    - ? (4 bytes)
    - Town Map ID (4 bytes)
    - Magick/Tech aptitude (4 bytes signed)
    - Light Scheme Override (4 bytes)
    - ? (4 bytes)
    - Music ID (4 bytes)
    - Ambient ID (4 bytes)
    - Blocked tile array (64 * 64 bits)
    - ??? (unknown bytes)
        # some data structure of environment / walls / traps
        # Every(?) item starts with value 119 (4 bytes)
        # File ends with number of items in this construct (4 bytes)
        # Note: Item size is not constant; perhaps: (walls 83 bytes, other 87 bytes)
    """
    unknown1_format = "I"
    unknown2_format = "I"
    unknown3_format = "I"
    town_map_format = "I"
    magick_aptitude_format = "i"
    light_scheme_format = "I"
    unknown4_format = "I"
    music_format = "I"
    ambient_format = "I"

    combined_format = "<" + "".join([unknown1_format, unknown2_format, unknown3_format, town_map_format, magick_aptitude_format,
                                     light_scheme_format, unknown4_format, music_format, ambient_format])

    combined_parser = FileStruct(combined_format)

    def __init__(self, file_path: str, lights: SectorLights, tiles: SectorTiles, roofs: SectorRoofs, scripts: SectorScripts,
                 town_map: int, magick_aptitude: int, light_scheme: int, music: int, ambient: int, blockades: SectorBlockades):

        self.file_path = file_path
        self.lights = lights
        self.tiles = tiles
        self.roofs = roofs
        self.scripts = scripts
        self.town_map = town_map
        self.magick_aptitude = magick_aptitude
        self.light_scheme = light_scheme
        self.music = music
        self.ambient = ambient
        self.blockades = blockades

    @classmethod
    def read(cls, sector_file_path: str) -> "Sector":

        with open(sector_file_path, "rb") as sector_file:

            lights = SectorLights.read_from(sector_file)
            tiles = SectorTiles.read_from(sector_file)
            roofs = SectorRoofs.read_from(sector_file)

            # Todo: Unknown data
            _ = FileStruct.cached_unpack_from_file("<4B", sector_file)

            scripts = SectorScripts.read_from(sector_file)

            # Todo: Unknown data
            _, _, _, town_map, magick_aptitude, light_scheme, _, music, ambient = cls.combined_parser.unpack_from_file(
                sector_file)

            blockades = SectorBlockades.read_from(sector_file)

            # Todo:
                # List of elements (environment, walls, traps, more?) of varying sizes

            return Sector(file_path=sector_file_path, lights=lights, tiles=tiles, roofs=roofs, scripts=scripts,
                          town_map=town_map, magick_aptitude=magick_aptitude, light_scheme=light_scheme, music=music,
                          ambient=ambient, blockades=blockades)


