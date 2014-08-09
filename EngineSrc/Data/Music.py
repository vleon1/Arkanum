import pyglet


class Music(object):

    def __init__(self, source):

        self.source = source

    def Play(self):

        player = pyglet.media.Player()
        player.queue(self.source)
        player.eos_action = pyglet.media.Player.EOS_LOOP

        player.play()

def Read(inputFilePath):

    source = pyglet.media.load(inputFilePath)

    return Music(source)
