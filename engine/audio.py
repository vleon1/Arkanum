from common.base import Base


# noinspection PyAbstractClass
class Audio(Base):

    def __init__(self, audio_path: str):

        self.audio_path = audio_path


class Sound(Audio):

    def load(self):
        raise NotImplemented()

    def play(self):
        raise NotImplemented()


class Music(Sound):
    pass
