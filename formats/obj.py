from formats.helpers import FileStruct
from formats.fields import Fields

import io
from typing import Tuple, List
from enum import IntEnum
from collections import OrderedDict
import struct

import numpy as np

class ObjectType(IntEnum):
    Wall = 0
    Portal = 1
    Container = 2
    Scenery = 3
    Projectile = 4
    Weapon = 5
    Ammo = 6
    Armor = 7
    Gold = 8
    Food = 9
    Scroll = 10
    Key = 11
    KeyRing = 12
    Written = 13
    Generic = 14
    Player = 15
    Critter = 16
    Trap = 17

class ObjectProperties(object):
    flags_parsers = (
        FileStruct("<H"),    # 0
        FileStruct("<H4B"),  # 1
        FileStruct("<H8B"),  # 2
        FileStruct("<H12B"), # 3
        FileStruct("<H16B"), # 4
        FileStruct("<H20B")  # 5
    )

    # Mapping from type to tuple of all (field name, parser)
    type_fields = (
        Fields.wall_fields,
        Fields.portal_fields,
        Fields.container_fields,
        Fields.scenery_fields,
        Fields.projectile_fields,
        Fields.weapon_fields,
        Fields.ammo_fields,
        Fields.armor_fields,
        Fields.gold_fields,
        Fields.food_fields,
        Fields.scroll_fields,
        Fields.key_fields,
        Fields.keyring_fields,
        Fields.written_fields,
        Fields.generic_fields,
        Fields.player_fields,
        Fields.critter_fields,
        Fields.trap_fields
    )

    # Size in bytes of included field flags.
    # len(Fields.type) / 32
    type_flags_length = (
        3, # 00 Wall
        3, # 01 Portal
        3, # 02 Container
        3, # 03 Scenery
        0, # 04 Projectile
        4, # 05 Weapon
        4, # 06 Ammo
        4, # 07 Armor
        4, # 08 Gold
        4, # 09 Food
        4, # 10 Scroll
        4, # 11 Key
        4, # 12 KeyRing
        4, # 13 Written
        4, # 14 Generic
        5, # 15 Player
        5, # 16 Critter
        3  # 17 Trap
    )

    @classmethod
    def read_from(cls, obj_file: io.FileIO, obj_type:ObjectType=None) -> "ObjectProperties":
        raise NotImplementedError()

        field_count, *raw_flags = cls.flags_parsers[cls.type_flags_length[obj_type]].unpack_from_file(obj_file)

        # Bytes to bit array.
        flags = np.fliplr(np.unpackbits(np.array(raw_flags, dtype=np.uint8)).reshape(-1, 8)).flatten()

        if (field_count != np.sum(flags)):
            raise RuntimeError("Field count doesn't match actual: %d versus %d" % (field_count, np.sum(flags)))

        # Parse fields from file
        raw_fields = {}
        for index in np.nonzero(flags)[0]:
            name, parse_func = cls.type_fields[obj_type][index]
            print(name)
            raw_fields[name] = parse_func(obj_file)


class ObjectIdentifier(object):
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

    def to_bytes(self) -> List[bytes]:

        # Perhaps better to just store the raw data during init.
        return (
            int.to_bytes(self.data[0], 4, 'little'),
            int.to_bytes(self.data[1], 2, 'little'),
            int.to_bytes(self.data[2], 2, 'little'),
            int.to_bytes(self.data[3], 2, 'big'),
            int.to_bytes(self.data[4], 6, 'big'),
        )


class Object(object):

    Type = ObjectType
    Properties = ObjectProperties
    Identifier = ObjectIdentifier

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

    full_format = "<" + "".join((constructor_type_format, unknown_data_format,
                                 raw_identifier_format, raw_type_format))
    full_parser = FileStruct(full_format)

    def __init__(self, version: int, type: ObjectType, identifier: ObjectIdentifier, properties: ObjectProperties):

        self.version = version
        self.type = type
        self.identifier = identifier

    @classmethod
    def read_from(cls, obj_file: io.FileIO) -> "Object":

        version, = cls.version_parser.unpack_from_file(obj_file)

        if (version != cls.valid_version):
            raise TypeError("Arkanum does not support object version %d" % version)

        constructor, unknown_data, raw_identifier, raw_type = cls.full_parser.unpack_from_file(obj_file)

        type = Object.Type(raw_type)

        properties = Object.Properties.read_from(obj_file, obj_type=type)


        return Object(version=version,
                      type=type,
                      identifier=Object.Identifier(raw_identifier),
                      properties=properties)

    def write_to(self, obj_file: io.FileIO) -> None:

        raise NotImplementedError()
        # self.version_parser.pack_into_file(self.version)
        # self.full_parser.pack_into_file(, unknown_data)
