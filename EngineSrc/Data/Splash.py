from glob import glob
from os import path
import random
import pyglet


class SplashLoop(pyglet.app.EventLoop):

    def __init__(self, loadingThread):

        super(SplashLoop, self).__init__()

        self.loadingThread = loadingThread

    def idle(self):

        if not self.loadingThread.is_alive():
            self.exit()
            return True

        return super(SplashLoop, self).idle()

class Splash(object):

    def __init__(self, texture):
        self.texture = texture
        self.videoSize = (texture.width, texture.height)

    def Render(self, window, stopCondition):

        drawLocation = window.CalculateCenterPosition(self.videoSize)

        def RespondToKey(key, modifiers):
            return True

        def RespondToMouse(x, y, button, modifiers):
            return True

        def DrawFrame():
            self.texture.blit(*drawLocation)

        def Finish():
            window.pop_handlers()

        splashLoop = SplashLoop(stopCondition)
        splashLoop.push_handlers(on_exit = Finish)

        window.push_handlers(on_key_press = RespondToKey,
                             on_mouse_press = RespondToMouse,
                             on_draw = DrawFrame)

        splashLoop.run()

def Read(splashesFolder):

    splashPaths = glob(path.join(splashesFolder, "*.bmp"))

    splashPath = random.choice(splashPaths)

    return Splash(pyglet.image.load(splashPath))


