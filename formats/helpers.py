from struct import Struct

from typing import List, Any, Union
import io


class FileStruct(Struct):

    _cached_parsers = {}

    def unpack_from_file(self, file: Union[io.FileIO, io.BufferedReader, io.BytesIO]) -> List[Any]:

        raw_data = file.read(self.size)
        return self.unpack(raw_data)

    def pack_to_file(self, file: Union[io.FileIO, io.BufferedReader, io.BytesIO], *values) -> None:
        packed = self.pack(*values)
        file.write(packed)

    @classmethod
    def get_cached_parser(cls, fmt: str) -> "FileStruct":

        if fmt not in cls._cached_parsers:
            cls._cached_parsers[fmt] = FileStruct(fmt)

        return cls._cached_parsers[fmt]

    @classmethod
    def cached_unpack_from_file(cls, fmt: str, file: Union[io.FileIO, io.BufferedReader, io.BytesIO]) -> List[Any]:

        return cls.get_cached_parser(fmt).unpack_from_file(file)

    @classmethod
    def cached_pack(cls, fmt: str, *values) -> bytes:

        return cls.get_cached_parser(fmt).pack(values)

    @classmethod
    def cached_pack_to_file(cls, fmt:str, file: Union[io.FileIO, io.BufferedReader, io.BytesIO], *values) -> None:

        cls.cached_pack_to_file(fmt, file, values)
