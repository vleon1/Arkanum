from formats.obj import Object

class MobileObject(Object):
    """
    An object that is expected to "change" during play, e.g it moves or it can be picked up by the
    player or some critter. In the file format it seems to defined as any other object.
    """

    @classmethod
    def read(cls, mob_file_path: str) -> "MobileObject":

        with open(mob_file_path, "rb") as mob_file:

            mob = cls.read_from(mob_file)
            mob.file_path = mob_file_path

            return mob

    def write(self, mob_file_path: str) -> None:

        with open(mob_file_path, "wb") as mob_file:

            self.write_to(mob_file)
