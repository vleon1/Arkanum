"""This module defines the format and parsing of script files."""
from formats.helpers import FileStruct
from formats.scr.lines import Line
from typing import List, Optional


class Script(object):
    """The class describes the format and serialization of a script.

    A Script contains a header with basic information and a series of lines.
    Scripts are stored as files with the extension ".scr".

    Attributes:
        file_path: Path to the file of the script.
        flags: Local flags of the script.
        counters: Local counters of  the sfcript.
        description: A description of the script.
        script_flags: Flags / settings of the script.
        lines: A list of script lines.
    """

    flags_format = "4B"
    counters_format = "4B"
    description_format = "40s"
    script_flags_format = "4B"
    num_lines_format = "I"
    unknown_data_format = "8B"
    full_format = (
        "<" + flags_format + counters_format + description_format +
        script_flags_format + num_lines_format + unknown_data_format)

    parser = FileStruct(full_format)

    def __init__(self,
                 file_path: str,
                 flags: Optional[List[int]]=None,
                 counters: Optional[List[int]]=None,
                 description: str="",
                 script_flags: Optional[List[int]]=None,
                 lines: Optional[List["Line"]]=None,
                 *args,
                 **kwargs):
        """Initialize the script.

        Arguments:
            file_path: Path to the script.
            flags: Local flag variables.
            counters: Local counter variables.
            description: Short description of the script.
            script_flags: Flag settings.
            lines: A list of script lines.
        """
        self.file_path = file_path
        self.flags = flags if flags else [0] * 4
        self.counters = counters if counters else [0] * 4
        self.description = description
        self.script_flags = script_flags if script_flags else [0] * 4
        self.lines = lines if lines else []

        # TODO: Identifiy unknown data
        self.unknown = {'args': args, 'kwargs': kwargs}

    @classmethod
    def read(cls, script_file_path: str) -> "Script":
        """Deserialize the file with the given path into a Script object.

        Arguments:
            script_file_path: Script file to deserialize.
        """
        with open(script_file_path, "rb") as script_file:

            header = cls.parser.unpack_from_file(script_file)
            flags = header[:4]
            counters = header[4:8]
            description = header[8][:header[8].index(b"\x00")].decode()
            script_flags = header[9:13]
            num_lines = header[13]
            unknown_data = header[14:]

            lines = []
            for line in range(num_lines):
                lines.append(Line.read_from(script_file))

            return cls(
                file_path=script_file_path,
                flags=flags,
                counters=counters,
                description=description,
                script_flags=script_flags,
                lines=lines,
                unknown_data=unknown_data)

    def write(self, script_file_path: str) -> None:
        """Serialize the script in to a file at the given path.

        Arguments:
            script_file_path: The path where the file should be written.
        """
        with open(script_file_path, "wb") as script_file:

            header = (*self.flags, *self.counters, self.description.encode(),
                      *self.script_flags, len(self.lines),
                      *self.unknown['kwargs']['unknown_data'])
            self.parser.pack_into_file(script_file, *header)
            for line in self.lines:
                line.write_to(script_file)
