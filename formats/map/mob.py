from formats.helpers import FileStruct

import io
from typing import Tuple

# From attaching a debug process to Arcanum.exe
# These are deduced from some globals that can be changed dynamically, therefore these might be
# wrong assumptions.
object_type_to_size = (
    3,  # 00
    3,  # 01
    3,  # 02
    3,  # 03
    ?,  # ??
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


class ObjectIdentifier(object):
    """
    The identifier is used as file name and must be unique for each object in a map.

    The binary format is peculier.
    First three values in the string representation are stored in little endian,
    the last two are either in big endian, or are single bytes put together.
    """

    string_format = "G_{:08X}_{:04X}_{:04X}_{:02X}{:02X}_{:02X}{:02X}{:02X}{:02X}{:02X}{:02X}".format

    identifier_format = "<I2H8B"
    identifier_parser = FileStruct(identifier_format)
    def __init__(self,
                data=None):

        if data:
            self.data = data
        else:
            raise NotImplemented()

    def __str__(self):
        return self.string_format(*self.data)

    @classmethod
    def read_from(cls, mob_file: io.FileIO) -> "ObjectIdentifier":

        data = cls.identifier_parser.unpack_from_file(mob_file)

        return ObjectIdentifier(data=data)

    def write(cls, mob_file: io.FileIO) -> None:

        self.identifier_parser.pack_into_file

class MobileObject(object):
    # From arcanum.exe:
    # Reads 4 bytes.
    # In debug called "object file format"
    # Checks for equallity with 119, if not doesnt parse.
    version_format = "<I"
    version_parser = FileStruct(version_format)
    valid_version = 119

    # Reads 24 bytes:
    # First 2 bytes decide which constructor(?) to use, useless (for now) since it is always 1 in .mob files.
    constructor_type_format = "H"
    # Next 16 bytes are unknown.
    unknown_data1_format = "16s"
    # Next 6 bytes are not even passed to the constructors.
    unknown_data2_format = "6s"

    # The default constructor reads 24 more bytes
    unknown_data3_format = "8s"  # unknown
    identifier_format = "16s"  # matches file name
    # IF that does not fail, reads 4 more bytes
    type_format = "I"  # object type  # 0 = wall, 2 = trap, 11 = critter ...
    # If that does not fail reads 2 more bytes
    size_format = "H"  # This many bytes will be allocated in addition to base(?) object

    # Based on type more bytes are read

    # Spaghetti assembly sad



    full_parser = FileStruct("<" + "".join(constructor_type_format, unknown_data1_format,
                                           unknown_data2_format, unknown_data3_format,
                                           identifier_format, type_format, unknown_data4_format))


    def __init__(self, file_path: str, version: int, identifier: ObjectIdentifier):

        self.file_path = file_path
        self.version = version
        self.identifier = identifier

    @classmethod
    def read(cls, mob_file_path: str) -> "MobileObject":

        with open(mob_file_path, "rb") as mob_file:

            version, = cls.version_parser.unpack_from_file(mob_file)

            if (version != cls.valid_version):
                raise TypeError("Arkanum does not support object version %d" % version)

            constructor, u1, identifier, type, u2 = cls.full_parser.unpack_from_file(mob_file)

            next_parser = FileStruct("<%ds" % object_type_to_size(type))
            next_parser.unpack_from_file(mob_file)

            print(identifier)



            # return MobileObject(file_path=mob_file_path, version=version, identifier=identifier)
            # return BlockedSectors(file_path=sector_blocked_file_path, blocked_sectors=blocked_sectors)
