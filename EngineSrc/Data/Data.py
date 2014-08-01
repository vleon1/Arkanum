from glob import glob
from os import path
import random

from DataTypes.Art import Art
from DataTypes.Mes import Mes
from DataTypes.Video import Video
from DataTypes.Image import Image
from DataTypes.Music import Music


class Data(object):

    def __init__(self, dataPath):

        self.dataPath = dataPath

    def GetSplashScreen(self, splashesSubFolder):

        splashesFolder = self.GetFilePath(splashesSubFolder)
        splashPaths = glob(path.join(splashesFolder, "*.bmp"))

        splashPath = random.choice(splashPaths)

        return Image.Read(splashPath)

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