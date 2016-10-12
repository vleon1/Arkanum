from common.base import Base


class Animation(Base):

    def __init__(self, animation_path: str):

        self.animation_path = animation_path

    def load(self):
        raise NotImplemented()

    def play(self):
        raise NotImplemented()
