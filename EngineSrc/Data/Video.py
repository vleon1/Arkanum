import pyglet

class VideoLoop(pyglet.app.EventLoop):

    def __init__(self, player):

        super(VideoLoop, self).__init__()

        self.player = player

    def idle(self):

        if self.player.get_texture() is None:
            self.exit()
            return True

        return super(VideoLoop, self).idle()

class Video(object):

    def __init__(self, source):

        self.source = source
        self.videoSize = (source.video_format.width, source.video_format.height)

    def Render(self, window):

        player = pyglet.media.Player()
        player.queue(self.source)

        drawLocation = window.CalculateCenterPosition(self.videoSize)

        def Run():
            player.play()

        def RespondToKey(key, modifiers):
            player.next()
            return True

        def RespondToMouse(x, y, button, modifiers):
            player.next()
            return True

        def DrawFrame():
            texture = player.get_texture()
            if texture is not None:
                texture.blit(*drawLocation)

        def Finish():
            window.pop_handlers()

        videoLoop = VideoLoop(player)
        videoLoop.push_handlers(on_enter = Run, on_exit = Finish)

        window.push_handlers(on_key_press = RespondToKey,
                             on_mouse_press = RespondToMouse,
                             on_draw = DrawFrame)

        videoLoop.run()

def Read(filePath):

    source = pyglet.media.load(filePath)

    return Video(source)
