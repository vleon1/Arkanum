import pyglet


class Window(pyglet.window.Window):

    def __init__(self, resolutionWidth, resolutionHeight, fullScreen):

        super(Window, self).__init__(caption = "pyRcanum",
                                     width = resolutionWidth, height = resolutionHeight, fullscreen = fullScreen)

    def CalculateCenterPosition(self, objectSize):

        size = self.get_size()

        def CalculateCenterPositionOnAxis(containerValue, objectValue):
            return (containerValue / 2) - (objectValue / 2) if objectValue < containerValue else 0

        objectXPosition = CalculateCenterPositionOnAxis(size[0], objectSize[0])
        objectYPosition = CalculateCenterPositionOnAxis(size[1], objectSize[1])

        return objectXPosition, objectYPosition
