import pygame


class Image(object):

    def __init__(self, texture):

        self.texture = texture

    def Render(self, screen):

        position = screen.CalculateCenterPosition(self.texture.get_size())

        screen.StartRender()
        screen.AddRender(self.texture, position)
        screen.EndRender()

def Read(inputFilePath):

    return Image(pygame.image.load(inputFilePath))
