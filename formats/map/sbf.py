from formats.helpers import FileStruct

from typing import List, Tuple

from collections.abc import Sequence

class BlockedSectors(Sequence):
    """
    If a sector is present in this object it is "blocked on the world map".
    """

    length_format = "<I"
    length_parser = FileStruct(length_format)

    data_format = "Q"

    def __init__(self,
                 file_path: str,
                 blocked_sectors: List[Tuple[int, int]]=[]):

        self.blocked_sectors = blocked_sectors
        self.file_path = file_path

    def __getitem__(self, index:int) -> Tuple[int, int]:
        return self.blocked_sectors[index]

    def __len__(self) -> int:
        return len(self.blocked_sectors)

    @classmethod
    def read(cls, sector_blocked_file_path: str) -> "SectorBlockades":

        with open(sector_blocked_file_path, "rb") as sector_blocked_file:

            length, = cls.length_parser.unpack_from_file(sector_blocked_file)

            raw_blocked_sectors_parser = FileStruct("<%d%s" % (length, cls.data_format))
            raw_blocked_sectors = raw_blocked_sectors_parser.unpack_from_file(sector_blocked_file)

            # Convert raw to real.
            blocked_sectors = []
            for raw_blocked_sector in raw_blocked_sectors:
                blocked_sectors.append((raw_blocked_sector & 0xFFF, raw_blocked_sector >> 26))

            return BlockedSectors(file_path=sector_blocked_file_path, blocked_sectors=blocked_sectors)

    def write(self, sector_blocked_file_path: str) -> None:

        with open(sector_blocked_file_path, "wb") as sector_blocked_file:

            length = len(self)
            if (length == 0):
                return

            self.length_parser.pack_into_file(sector_blocked_file, length)

            # Convert real to raw.
            raw_blocked_sectors = []
            for sector_x, sector_y in self:
                raw_blocked_sectors.append(sector_x | (sector_y << 26))

            raw_blocked_sectors_parser = FileStruct("<%d%s" % (length, self.data_format))
            raw_blocked_sectors_parser.pack_into_file(sector_blocked_file, *raw_blocked_sectors)
