from formats.helpers import FileStruct
from formats.obj import Object

import io

from typing import List, Any, Tuple


class SectorLights(object):
    """
    Binary file format:
    - Light count (4 bytes)
    - Light (48 bytes) * Light count
    """
    count_format = "<I"

    raw_format = "48s"

    count_parser = FileStruct(count_format)

    def __init__(self, raw_lights: List[Any]):

        self.raw_lights = raw_lights

    def __len__(self) -> int:

        return len(self.raw_lights)

    def __getitem__(self, index: int) -> int:

        return self.raw_lights[index]

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorLights":

        count, = cls.count_parser.unpack_from_file(sector_file)

        if (count > 0):
            fmt = "<" + cls.raw_format * count
            raw_lights = FileStruct(fmt).unpack_from_file(sector_file)
        else:
            raw_lights = []

        return SectorLights(raw_lights)

    def write_to(self, sector_file: io.FileIO) -> None:

        count = len(self.raw_lights)
        self.count_parser.pack_into_file(sector_file, count)

        if (count > 0):
            fmt = "<" + self.raw_format * count
            FileStruct(fmt).pack_into_file(sector_file, *self.raw_lights)


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

        raw_tiles_data = self.raw_tiles_parser.pack_into_file(sector_file, *self.raw_tiles)


class SectorRoofs(object):
    """
        Binary file format:
    - Roof (4 bytes) * 256
    """

    type_format = "<I"
    raw_roofs_format = "<256I"

    type_parser = FileStruct(type_format)
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

        type, = cls.type_parser.unpack_from_file(sector_file)

        if type == 0:
            raw_roofs = cls.raw_roofs_parser.unpack_from_file(sector_file)
        else:
            raw_roofs = []

        return SectorRoofs(type=type, raw_roofs=raw_roofs)

    def write_to(self, sector_file: io.FileIO) -> None:

        self.type_parser.pack_into_file(sector_file, self.type)

        if self.type == 0:
            self.raw_roofs_parser.pack_into_file(sector_file, *self.raw_roofs)


class SectorTileScripts(object):
    """
    Binary file format:
    - Tile scripts count (4 bytes)
    - Tile script (24 bytes) * count

    Binary file format per tile script:
    - ? (4 bytes)
    - Index of tile in sector (2 bytes)
    - ? (2 bytes)
    - Flags (4 bytes)
    - Counters (4 bytes)
    - Script ID (4 bytes)
    - ? (4 bytes)
    """
    count_format = "<I"
    raw_format = "24s"

    count_parser = FileStruct(count_format)

    def __init__(self, raw_scripts: List[Any]=[]):

        self.raw_scripts = raw_scripts

    def __len__(self) -> int:

        return len(self.raw_scripts)

    def __getitem__(self, index: int) -> int:

        return self.raw_scripts[index]

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorTileScripts":

        count, = cls.count_parser.unpack_from_file(sector_file)

        if (count > 0):
            fmt = "<" + cls.raw_format * count
            raw_scripts = FileStruct(fmt).unpack_from_file(sector_file)
        else:
            raw_scripts = []

        return SectorTileScripts(raw_scripts=raw_scripts)

    def write_to(self, sector_file: io.FileIO) -> None:

        count = len(self.raw_scripts)
        count_data = self.count_parser.pack_into_file(sector_file, count)

        if (count > 0):
            fmt = "<" + self.raw_format * count
            raw_data = FileStruct(fmt).pack_into_file(sector_file, *self.raw_scripts)

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

        self.raw_blockades_parser.pack_into_file(sector_file, self.raw_blockades)


class SectorInfo(object):
    """
    Binary file format:
    - Type (4 bytes)
    - Info (varying bytes)
    
    type 0:
        - Nothing
    type 1:
        - Script tile count (4 bytes)
            # List of tile scripts (n * 24 bytes)
    type 2:
        - all of type 1 
        - Sector Script Flags (4 bytes)
        - Sector Script Counters (4 * 1 byte)
        - Sector Script ID (4 bytes)
    type 3:
        - all of type 2
        - Town Map ID (4 bytes)
        - Magick/Tech aptitude (4 bytes signed)
        - Light Scheme (4 bytes)
        - NULL (4 bytes)
        - Music ID (4 bytes)
        - Ambient ID (4 bytes)
    type 4: (Default, WorldEd always(?) saves as type 4)
        - all of type 3
        - Blocked tile array (64 * 64 bits)
    """

    # Figure out whether unchanging bits have meaning
    class Type(object):
        NO_INFO      = 0x00AA0000
        TILE_SCRIPTS = 0x00AA0001
        ALL_SCRIPTS  = 0x00AA0002
        BASIC        = 0x00AA0003
        FULL         = 0x00AA0004

    type_format = "<I"
    type_parser = FileStruct(type_format)

    script_flags_format = "I"
    script_counters_format = "I"
    script_id_format = "I"
    sector_script_format = script_flags_format + script_counters_format + script_id_format

    town_map_format = "I"
    magick_aptitude_format = "i"
    light_scheme_format = "I"
    unknown_format = "I" # Always 0
    music_format = "I"
    ambient_format = "I"
    blockades_format = "512B"

    basic_format = (town_map_format + magick_aptitude_format + light_scheme_format +
                    unknown_format + music_format + ambient_format)

    sector_script_parser = FileStruct("<" + sector_script_format)
    basic_parser = FileStruct("<" + sector_script_format + basic_format)
    full_parser = FileStruct("<" + sector_script_format + basic_format + blockades_format)

    
    def __init__(self,
                 type: int=Type.FULL,
                 tile_scripts: SectorTileScripts=None,
                 sector_script: (int, int, int)=(0,0,0),
                 town_map: int=0,
                 magick_aptitude: int=0,
                 light_scheme: int=0,
                 music: int=0,
                 ambient: int=0,
                 blockades: List[Any]=[]):

        self.type = type
        self.tile_scripts = tile_scripts
        self.sector_script = sector_script
        self.town_map = town_map
        self.magick_aptitude = magick_aptitude
        self.light_scheme = light_scheme
        self.music = music
        self.ambient = ambient
        self.blockades = blockades


    def __len__(self) -> int:

        return len(self.raw_blockades)

    def __getitem__(self, index: int) -> int:

        return self.raw_blockades[index]

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorInfo":

        type, = cls.type_parser.unpack_from_file(sector_file)

        if type == cls.Type.NO_INFO:
            return SectorInfo(type=type)

        tile_scripts = SectorTileScripts.read_from(sector_file)

        if type == cls.Type.TILE_SCRIPTS:
            return SectorInfo(type=type, tile_scripts=tile_scripts)

        elif type == cls.Type.ALL_SCRIPTS:  
            sector_script = cls.sector_script_parser.unpack_from_file(sector_file)
            return SectorInfo(type=type, tile_scripts=tile_scripts, sector_script=sector_script)

        elif type == cls.Type.BASIC:
            (sector_script_flags, sector_script_counters, sector_script_id, town_map,
             magick_aptitude, light_scheme, _, music, ambient
            ) = cls.basic_parser.unpack_from_file(sector_file)

            sector_script = (sector_script_flags, sector_script_counters, sector_script_id)

            return SectorInfo(type=type, tile_scripts=tile_scripts, sector_script=sector_script, 
                              town_map=town_map, magick_aptitude=magick_aptitude,
                              light_scheme=light_scheme, music=music, ambient=ambient)

        elif type == cls.Type.FULL:
            (sector_script_flags, sector_script_counters, sector_script_id, town_map,
             magick_aptitude, light_scheme, _, music, ambient, *blockades
            ) = cls.full_parser.unpack_from_file(sector_file)

            sector_script = (sector_script_flags, sector_script_counters, sector_script_id)

            return SectorInfo(type=type, tile_scripts=tile_scripts, sector_script=sector_script,
                              town_map=town_map, magick_aptitude=magick_aptitude,
                              light_scheme=light_scheme, music=music, ambient=ambient,
                              blockades=blockades)

        else:
            raise NotImplementedError("Can not handle unknown type %d" % (type))

    def write_to(self, sector_file: io.FileIO) -> None:

        self.type_parser.pack_into_file(sector_file, self.type)

        if self.type == self.Type.NO_INFO:
            return

        self.tile_scripts.write_to(sector_file)

        if self.type == self.Type.ALL_SCRIPTS:  
            self.sector_script_parser.pack_into_file(sector_file, *self.sector_script)

        elif self.type == self.Type.BASIC:
            self.basic_parser.pack_into_file(sector_file, *self.sector_script, self.town_map,
                                             self.magick_aptitude, self.light_scheme, 0,
                                             self.music, self.ambient)

        elif self.type == self.Type.FULL:
            self.full_parser.pack_into_file(sector_file, *self.sector_script, self.town_map,
                                            self.magick_aptitude, self.light_scheme, 0,
                                            self.music, self.ambient, *self.blockades)


class SectorObjects(object):

    length_format = "I"
    length_parser = FileStruct("<" + length_format)

    def __init__(self, objects: List[Any]=[]):

        self.objects = objects

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, index: int) -> Object:
        return self.objects[index]

    def __iter__(self):
        return iter(self.objects)

    @classmethod
    def read_from(cls, sector_file: io.FileIO) -> "SectorInfo":

        # Save current position in file
        tell = sector_file.tell()

        # Go to end of file minus size of length.
        sector_file.seek(-cls.length_parser.size, 2)

        length,  = cls.length_parser.unpack_from_file(sector_file)

        print(length)

        objects = []

        if length:
            # Go back to saved position
            sector_file.seek(tell)

            for _ in range(length):
                objects.append(Object.read_from(sector_file))

        return SectorObjects(objects=objects)

    def write_to(self, sector_file: io.FileIO) -> None:

        for obj in self:
            obj.write_to(sector_file)

        self.length_parser.pack_into_file(sector_file, len(self))


class Sector(object):
    """
    Binary file format (everything unsigned unless explicitly mentioned): 
    - Lights (4 bytes + count * 24 bytes)
    - Tiles (4096 bytes)
    - Roofs (1024 bytes)
    - Info (4 bytes + varying bytes based on type)
    - Objects (varying bytes + 4 bytes)
        - Since objects have varying sizes each needs to be read one by one.
        - After all objects the file ends with the number of objects (4 bytes).
    """

    def __init__(self, file_path: str, lights: SectorLights, tiles: SectorTiles, roofs: SectorRoofs,
                 info: SectorInfo, objects: SectorObjects):

        self.file_path = file_path
        self.lights = lights
        self.tiles = tiles
        self.roofs = roofs
        self.info = info
        self.objects = objects

    @classmethod
    def read(cls, sector_file_path: str) -> "Sector":

        with open(sector_file_path, "rb") as sector_file:

            lights = SectorLights.read_from(sector_file)
            tiles = SectorTiles.read_from(sector_file)
            roofs = SectorRoofs.read_from(sector_file)
            info = SectorInfo.read_from(sector_file)
            objects = SectorObjects.read_from(sector_file)

            return Sector(file_path=sector_file_path, lights=lights, tiles=tiles, roofs=roofs,
                          info=info, objects=objects)

    def write(self, sector_file_path: str) -> None:

        with open(sector_file_path, "wb") as sector_file:

            self.lights.write_to(sector_file)
            self.tiles.write_to(sector_file)
            self.roofs.write_to(sector_file)
            self.info.write_to(sector_file)
            self.objects.write_to(sector_file)



