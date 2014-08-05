import pygame
import pyglet


class Window(object):

    def __init__(self, resolutionWidth, resolutionHeight, fullScreen):

        self.window = pyglet.window.Window(caption = "pyRcanum",
                                           width = resolutionWidth, height = resolutionHeight) #, fullscreen = fullScreen)

        self.size = self.window.get_size()

    def CalculateCenterPosition(self, objectSize):

        def CalculateCenterPositionOnAxis(containerValue, objectValue):
            return (containerValue / 2) - (objectValue / 2) if objectValue < containerValue else 0

        objectXPosition = CalculateCenterPositionOnAxis(self.size[0], objectSize[0])
        objectYPosition = CalculateCenterPositionOnAxis(self.size[1], objectSize[1])

        return objectXPosition, objectYPosition

    def StartRender(self):
        self.window.fill((0,0,0))

    def AddRender(self, texture, position):
        self.window.blit(texture, position)

    def EndRender(self):
        pygame.display.flip()
