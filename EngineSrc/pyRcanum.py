import threading
import pyglet
from Config import Config
from EngineSrc.Data import Data
from EngineSrc.Engine.Menu import Menu
from EngineSrc.Engine.Window import Window


class Arcanum(object):

    def __init__(self, configPath, applicationPath):

        intArguments = ["resolutionWidth", "resolutionHeight", "fullScreen"]
        config = Config.Read(configPath, intArguments = intArguments)

        dataPath = config.dataPathTemplate.format(applicationPath = applicationPath)
        self.data = Data(dataPath)

        self.window = Window(config.resolutionWidth, config.resolutionHeight, config.fullScreen)

        self.menu = None

    def Run(self):

        self.HandleLoading()

        self.HandleMenu()

    def HandleLoading(self):

        # Start loading data in the background
        self.Load()
        loadingThread = threading.Thread(target = self.Load)
        #loadingThread.start()

        # Start playing video while loading stuff
        self.data.GetVideoFile("data/movies/SierraLogo.bik").Render(self.window)
        self.data.GetVideoFile("data/movies/TroikaLogo.bik").Render(self.window)

        # Show splash if still loading stuff and until it ends.
        self.data.GetSplashScreen("data/art/splash").Render(self.window, loadingThread)

        # Play menu intro movie when loading is finished.
        self.data.GetVideoFile("modules/Arcanum/movies/50000.bik").Render(self.window)

    def Load(self):

        self.menu = Menu(self.data, self.window)

    def HandleMenu(self):

        music = self.data.GetMusicFile("modules/Arcanum/sound/music/Arcanum.mp3")
        music.Play()

        cursorImage = self.data.GetArtFile("data/art/interface/cursor.art").Image()
        cursor = pyglet.window.ImageMouseCursor(cursorImage.Texture(), hot_y = cursorImage.info.size[1] - 1)
        self.window.set_mouse_cursor(cursor)
        self.window.push_handlers(on_mouse_motion = lambda x, y, dx, dy: self.window.draw_mouse_cursor(), on_draw = lambda: self.menu.Render(self.window))

        pyglet.app.run()
