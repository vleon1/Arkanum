from typing import List

from common.base import Base

from engine.audio import Music

from logic.actor import Actor


class Area(Base):

    def __init__(self, music: Music, actors: List[Actor]):

        self.music = music
        self.actors = actors

    def load(self):

        self.music.load()
        for actor in self.actors:
            actor.load()

        raise NotImplemented()

    def play(self):

        self.music.play()
        for actor in self.actors:
            actor.play()

        raise NotImplemented()
