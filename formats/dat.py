from formats.helpers import FileStruct
import io
import zlib
from Collections import OrderedDict

from typing import Dict, Iterable


class DatFooter(object):

    class Constants(object):
        marker = b"1TAD"

    guid_format = "16s"
    marker_format = "4s"  # Should always equal "1TAD" ?
    file_names_size_format = "I"  # Total allocation size for file names (we will probably ignore this)
    footer_plus_entries_size_format = "I"
    full_format = "<" + guid_format + marker_format + file_names_size_format + footer_plus_entries_size_format

    parser = FileStruct(full_format)

    def __init__(self, guid: bytes, marker: bytes, file_names_size: int, footer_plus_entries_size: int):

        assert marker == self.Constants.marker

        self.guid = guid
        self.file_names_size = file_names_size
        self.footer_plus_entries_size = footer_plus_entries_size

    @classmethod
    def read_from(cls, dat_file: io.FileIO) -> "DatFooter":

        guid, marker, file_names_size, footer_plus_entries_size = DatFooter.parser.unpack_from_file(dat_file)

        return DatFooter(guid=guid, marker=marker, file_names_size=file_names_size,
                         footer_plus_entries_size=footer_plus_entries_size)

    @property
    def marker(self) -> str:
        return self.Constants.marker


class DatEntry(object):

    class Flags(object):
        is_compressed = 0x002
        is_directory = 0x400

    padding_format = "4x"  # Its always saved as zero, but in memory its usually a 32bit pointer to the name.
    flags_format = "I"
    full_size_format = "I"
    compressed_size_format = "I"
    location_format = "I"
    full_format = "<" + padding_format + flags_format + full_size_format + compressed_size_format + location_format

    parser = FileStruct(full_format)

    def __init__(self, flags: int, full_size: int, compressed_size: int, location: int):

        self.is_compressed = bool(flags & self.Flags.is_compressed)
        self.is_directory = bool(flags & self.Flags.is_directory)
        self.full_size = full_size
        self.compressed_size = compressed_size
        self.location = location

    @classmethod
    def read_from(cls, dat_file: io.FileIO) -> "DatEntry":

        flags, full_size, compressed_size, location = DatEntry.parser.unpack_from_file(dat_file)

        return DatEntry(flags=flags, full_size=full_size, compressed_size=compressed_size, location=location)


class Dat(object):

    number_of_entries_parser = FileStruct("<I")
    file_name_length_parser = FileStruct("<I")

    def __init__(self, dat_file: io.FileIO, footer: DatFooter, name_to_entry: Dict[str, DatEntry]):

        self.dat_file = dat_file

        self.footer = footer

        self.name_to_entry = name_to_entry

    @classmethod
    def open(cls, dat_file_path: str) -> "Dat":

        dat_file = open(dat_file_path, "rb")

        dat_file.seek(-DatFooter.parser.size, io.SEEK_END)

        footer = DatFooter.read_from(dat_file)

        dat_file.seek(-footer.footer_plus_entries_size, io.SEEK_END)
        number_of_entries, = cls.number_of_entries_parser.unpack_from_file(dat_file)

        name_to_entry = OrderedDict()  # type: Dict[str, DatEntry]

        for _ in range(number_of_entries):

            file_name_length, = cls.file_name_length_parser.unpack_from_file(dat_file)
            file_name = dat_file.read(file_name_length - 1).decode()  # we don't want to save the last null
            dat_file.read(1)  # to skip the null byte

            name_to_entry[file_name] = DatEntry.read_from(dat_file)

        return Dat(dat_file=dat_file, footer=footer, name_to_entry=name_to_entry)

    def __contains__(self, name: str) -> bool:
        return name in self.name_to_entry

    def __getitem__(self, name: str) -> bytes:

        entry = self.name_to_entry[name]

        if entry.is_directory:
            return b""

        self.dat_file.seek(entry.location, io.SEEK_SET)

        raw_data = self.dat_file.read(entry.compressed_size)

        if entry.is_compressed:
            return zlib.decompress(raw_data)
        else:
            return raw_data

    def keys(self) -> Iterable[str]:
        return self.name_to_entry.keys()
