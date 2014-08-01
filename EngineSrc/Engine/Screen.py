import pygame


class Screen(object):

    def __init__(self, screen):
        self.screen = screen
        self.size = self.screen.get_size()

    def CalculateCenterPosition(self, objectSize):

        def CalculateCenterPositionOnAxis(containerValue, objectValue):
            return (containerValue / 2) - (objectValue / 2) if objectValue < containerValue else 0

        objectXPosition = CalculateCenterPositionOnAxis(self.size[0], objectSize[0])
        objectYPosition = CalculateCenterPositionOnAxis(self.size[1], objectSize[1])

        return objectXPosition, objectYPosition

    def StartRender(self):
        self.screen.fill((0,0,0))

    def AddRender(self, texture, position):
        self.screen.blit(texture, position)

    def EndRender(self):
        pygame.display.flip()
