import threading
import pyglet

from Config import Config
from EngineSrc.Data.Data import Data
# from EngineSrc.Engine.Menu import Menu
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

        #self.HandleMenu()

    def HandleLoading(self):

        # loadingThread = threading.Thread(target = self.Load)
        # loadingThread.start()

        # Start playing video while loading stuff
        self.data.GetVideoFile("data/movies/SierraLogo.bik").Render(self.window)
        #self.data.GetVideoFile("data/movies/TroikaLogo.bik").Render(self.window)

        pyglet.app.run()

        # Show splash if still loading stuff and until it ends.
        # splash = self.data.GetSplashScreen("data/art/splash")
        # splash.Render(self.screen)
        #
        # while loadingThread.is_alive():
        #     pass
        #
        # self.data.GetVideoFile("modules/Arcanum/movies/50000.mpg").Render(self.screen)

    def Load(self):

        pass # self.menu = Menu(self.data, self.screen)

    def HandleMenu(self):

        pass
        # music = self.data.GetMusicFile("modules/Arcanum/sound/music/Arcanum.mp3")
        # music.Play()
        #
        # cursor = self.data.GetArtFile("data/art/interface/cursor.art").Image().Texture()
        #
        # self.screen.StartRender()
        # self.menu.AddRender(self.screen, self.menu.startSentences)
        # self.screen.AddRender(cursor, pygame.mouse.get_pos())
        # self.screen.EndRender()
        #
        # while 1:
        #
        #     event = pygame.event.poll()
        #
        #     if event.type == pygame.QUIT:
        #         return
        #
        #     if event.type == pygame.KEYUP:
        #
        #         if event.key == pygame.K_ESCAPE:
        #             return
        #
        #     if event.type == pygame.MOUSEMOTION:
        #
        #         self.screen.StartRender()
        #         self.menu.AddRender(self.screen, self.menu.startSentences)
        #         self.screen.AddRender(cursor, event.pos)
        #         self.screen.EndRender()
