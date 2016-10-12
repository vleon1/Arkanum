from common.base import Base

from engine.animation import Animation


# noinspection PyAbstractClass
class Actor(Base):

    def __init__(self, base_animation: Animation):

        self.base_animation = base_animation


class Static(Actor):

    def load(self):
        raise NotImplemented()

    def play(self):
        raise NotImplemented()


class Creature(Actor):

    def load(self):
        raise NotImplemented()

    def play(self):
        raise NotImplemented()
