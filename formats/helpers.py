from struct import Struct

from typing import List, Any, Union
import io


class FileStruct(Struct):

    def unpack_from_file(self, file: Union[io.FileIO, io.BufferedReader, io.BytesIO]) -> List[Any]:

        raw_data = file.read(self.size)
        return self.unpack(raw_data)
