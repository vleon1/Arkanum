from struct import Struct

from typing import List, Any
import io


class FileStruct(Struct):

    def unpack_from_file(self, file: io.FileIO) -> List[Any]:

        raw_data = file.read(self.size)
        return self.unpack(raw_data)
