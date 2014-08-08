import pyglet


class Video(object):

    def __init__(self, sources):

        self.player = pyglet.media.Player()

        for source in sources:
            self.player.queue(source)

    def RespondToKey(self, key, modifiers):
        self.FinishPlaying()
        return True

    def RespondToMouse(self, x, y, button, modifiers):
        self.FinishPlaying()
        return True

    def DrawFrame(self):

        texture = self.player.get_texture()
        texture.blit(0, 0)

    def FinishPlaying(self):
        self.player.next()

    def Render(self, window):

        window.push_handlers(on_key_press = self.RespondToKey,
                             on_mouse_press = self.RespondToMouse,
                             on_draw = self.DrawFrame)

        self.player.push_handlers(on_player_eos = lambda: window.pop_handlers())

        self.player.play()

def Read(filePaths):

    sources = map(lambda x: pyglet.media.load(x), filePaths)

    return Video(sources)
