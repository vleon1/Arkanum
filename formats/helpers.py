from struct import Struct

from typing import List, Any, Union
import io
import enum


class FileStruct(Struct):

    def unpack_from_file(self, file: Union[io.FileIO, io.BufferedReader, io.BytesIO]) -> List[Any]:

        raw_data = file.read(self.size)
        return self.unpack(raw_data)

    def pack_into_file(self, file: Union[io.FileIO, io.BufferedReader, io.BytesIO], *values) -> None:

        packed = self.pack(*values)
        file.write(packed)


class IntEnumPlus(enum.IntEnum):
    """IntEnum whose constructor can take additional attributes.

    The implementation allows for additional attributes that do not affect the
    logical value of the enum.
    """

    def __new__(cls, value: int, *args: List[Any]) -> "IntEnumPlus":
        """Instantiate a new member."""
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj


def name(name):
    """Give a class a different name."""
    def decorator(cls):
        cls.__name__ = name
        return cls
    return decorator
