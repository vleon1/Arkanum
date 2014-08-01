import threading
import pygame
import pygame.mixer

from Config import Config
from EngineSrc.Data.Data import Data
from EngineSrc.Engine.Menu import Menu
from EngineSrc.Engine.Screen import Screen


class Arcanum(object):

    def __init__(self, configPath, applicationPath):

        intArguments = ["resolutionWidth", "resolutionHeight", "fullScreen"]
        config = Config.Read(configPath, intArguments = intArguments)

        dataPath = config.dataPathTemplate.format(applicationPath = applicationPath)
        self.data = Data(dataPath)

        pygame.init()
        pygame.display.set_caption("pyRcanum")
        pygame.mouse.set_visible(False)

        size = (config.resolutionWidth, config.resolutionHeight)
        flags = pygame.FULLSCREEN if config.fullScreen else 0
        self.screen = Screen(pygame.display.set_mode(size, flags))

        self.menu = None

    def Run(self):

        self.HandleLoading()

        self.HandleMenu()

    def HandleLoading(self):

        loadingThread = threading.Thread(target = self.Load)
        loadingThread.start()

        # Start playing video while loading stuff
        self.data.GetVideoFile("data/movies/SierraLogo.mpg").Render(self.screen)
        self.data.GetVideoFile("data/movies/TroikaLogo.mpg").Render(self.screen)

        # Show splash if still loading stuff and until it ends.
        splash = self.data.GetSplashScreen("data/art/splash")
        splash.Render(self.screen)

        while loadingThread.is_alive():
            pass

        self.data.GetVideoFile("modules/Arcanum/movies/50000.mpg").Render(self.screen)

    def Load(self):

        self.menu = Menu(self.data, self.screen)

    def HandleMenu(self):

        music = self.data.GetMusicFile("modules/Arcanum/sound/music/Arcanum.mp3")
        music.Play()

        cursor = self.data.GetArtFile("data/art/interface/cursor.art").Image().Texture()

        self.screen.StartRender()
        self.menu.AddRender(self.screen, self.menu.startSentences)
        self.screen.AddRender(cursor, pygame.mouse.get_pos())
        self.screen.EndRender()

        while 1:

            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEMOTION:

                self.screen.StartRender()
                self.menu.AddRender(self.screen, self.menu.startSentences)
                self.screen.AddRender(cursor, event.pos)
                self.screen.EndRender()
