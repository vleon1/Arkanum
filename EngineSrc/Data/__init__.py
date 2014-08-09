from os import path
import Art

import Splash, Mes, Music, Video

class Data(object):

    def __init__(self, dataPath):

        self.dataPath = dataPath

    def GetSplashScreen(self, splashesSubFolder):

        splashesFolder = self.GetFilePath(splashesSubFolder)

        return Splash.Read(splashesFolder)

    def GetVideoFile(self, relativeFilePath):

        filePath = self.GetFilePath(relativeFilePath)
        return Video.Read(filePath)

    def GetMusicFile(self, relativeFilePath):

        filePath = self.GetFilePath(relativeFilePath)
        return Music.Read(filePath)

    def GetArtFile(self, relativeFilePath):

        filePath = self.GetFilePath(relativeFilePath)
        return Art.Read(filePath)

    def GetMesFile(self, relativeFilePath):

        filePath = self.GetFilePath(relativeFilePath)
        return Mes.Read(filePath)

    def GetFilePath(self, relativePath):

        return path.join(self.dataPath, relativePath)