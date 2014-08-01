import pygame


class Music(object):

    def __init__(self, musicPath):

        self.musicPath = musicPath

    def Play(self):

        pygame.mixer.music.load(self.musicPath)
        pygame.mixer.music.play(-1)

def Read(inputFilePath):

    return Music(inputFilePath)
