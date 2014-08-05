import pyglet


class Video(object):

    def __init__(self, source):

        self.source = source

        self.player = pyglet.media.Player()
        self.player.queue(source)

    def Render(self, window):

        self.player.play()

        firstTexture = self.player.get_texture()

        x, y = window.CalculateCenterPosition((firstTexture.width, firstTexture.height))

        window.window.set_handler("on_draw", lambda: self.player.get_texture().blit(x, y))

def Read(inputFilePath):

    data = pyglet.media.load(inputFilePath)

    return Video(data)
