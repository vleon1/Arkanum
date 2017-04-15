from formats.helpers import FileStruct

import io
from typing import Tuple
from enum import Enum
import struct

# From attaching a debug process to Arcanum.exe
# These are deduced from some globals that can be changed dynamically, therefore these might be
# wrong assumptions.
object_type_to_size = (
    3,  # 00
    3,  # 01
    3,  # 02
    3,  # 03
    0,  # ??
    4,  # 05
    4,  # 06
    4,  # 07
    4,  # 08
    4,  # 09
    4,  # 10
    4,  # 11
    4,  # 12
    4,  # 13
    4,  # 14
    5,  # 15
    5,  # 16
    3   # 17
)

# arcanum.exe:4e44f0
object_type_to_size2 = (
    0,  # 00
    0,  # 01
    0,  # 02
    4,  # 03
    9,  # 04
    1,  # 05
    1,  # 06
    1,  # 07
    1,  # 08
    1,  # 09
    1,  # 10
    5,  # 11
    19,  # 12
    1,  # 13
    0,  # 14
    0,  # 15
    0,  # 16
    0   # 17
)

class Object(object):

    class Type(Enum):
        Wall = 0
        Portal = 1
        Container = 2
        Scenery = 3
        Projectile = 4
        Weapon = 5
        Ammo = 6
        Armor = 7
        Money = 8
        Food = 9
        Scroll = 10
        Key = 11
        # Key Ring = 12
        Written = 13
        Generic = 14
        Player = 15
        Critter = 16
        Trap = 17

    class Identifier(object):
        format = "G_{:08X}_{:04X}_{:04X}_{:04X}_{:012X}".format

        def __init__(self, raw_data):
            self.data = (
                int.from_bytes(raw_data[:4], 'little'),
                int.from_bytes(raw_data[4:6], 'little'),
                int.from_bytes(raw_data[6:8], 'little'),
                int.from_bytes(raw_data[8:10], 'big'),
                int.from_bytes(raw_data[10:], 'big'),
            )

        def __repr__(self):
            return self.format(*self.data)

        def __eq__(self, other):
            self.data == other.data

        def to_bytes(self):

            # Perhaps better to just store the raw data during init.
            return (
                int.to_bytes(self.data[0], 'little'),
                int.to_bytes(self.data[1], 'little'),
                int.to_bytes(self.data[2], 'little'),
                int.to_bytes(self.data[3], 'big'),
                int.to_bytes(self.data[4], 'big'),
            )

    version_format = "<I"
    version_parser = FileStruct(version_format)
    valid_version = 119

    # First 2 bytes decide which constructor(?) to use, 1 for .mob files, -1 for .pro files
    # There is also something called obj dif file, probably patch related.
    constructor_type_format = "H"

    # .mob files:
    unknown_data_format = "30s"
    raw_identifier_format = "16s"  # matches file name, unique per entity per map
    raw_type_format = "I"  # If that does not fail reads 2 more bytes
    size_format = "H"  # This many bytes will be needed in addition to base(?) object

    # Based on type more bytes are read
    full_format = "<" + "".join((constructor_type_format, unknown_data_format,
                                 raw_identifier_format, raw_type_format, size_format))
    full_parser = FileStruct(full_format)

    def __init__(self, file_path: str, version: int, type: Type, identifier: Identifier):

        self.file_path = file_path
        self.version = version
        self.type = type
        self.identifier = identifier

    @classmethod
    def read_from(cls, obj_file: io.FileIO) -> "Object":

        version, = cls.version_parser.unpack_from_file(obj_file)

        if (version != cls.valid_version):
            raise TypeError("Arkanum does not support object version %d" % version)

        constructor, unknown_data, raw_identifier, raw_type, size = cls.full_parser.unpack_from_file(obj_file)

        return Object(file_path=obj_file_path,
                      version=version,
                      type=Object.Type(raw_type),
                      identifier=Object.Identifier(raw_identifier))


    def write_to(self, obj_file: io.FileIO) -> None:

        self.version_parser.pack_into_file(self.version)

        # self.full_parser.pack_into_file(, unknown_data)
