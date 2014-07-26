from struct import Struct
import tarfile

import pygame

palletPixelReader = Struct("<" + "BBB" * 256)

class TartColorImage(pygame.Surface):

    def __init__(self, baseSurface, pallet, metaData):

        #baseSurface.set_palette(pallet)

        self.surface = baseSurface.convert()
        self.metaData = metaData

class MetaData(object):

    def __init__(self, metaDataDictionary):

        self.x = metaDataDictionary["x"]
        self.y = metaDataDictionary["y"]

        self.dX = metaDataDictionary["dX"]
        self.dY = metaDataDictionary["dY"]

class TartData(object):

    def __init__(self, tartType, pallets, surfaces, metaDatas, numberOfPositions, numberOfFrames):

        self.type = tartType

        self.pallets = pallets
        self.surfaces = surfaces
        self.metaDatas = metaDatas

        self.numberOfPositions = numberOfPositions
        self.numberOfFrames = numberOfFrames

    def GetImage(self, positionIndex, frameIndex, palletIndex):

        surface = self.surfaces[positionIndex * self.numberOfFrames + frameIndex].copy()
        metaData = self.metaDatas[positionIndex * self.numberOfFrames + frameIndex]
        pallet = self.pallets[palletIndex]

        return TartColorImage(surface, pallet, metaData)

def Open(tartFilePath):

    with tarfile.open(tartFilePath) as tartFile:

        header = ReadMetaData(tartFile.extractfile("header.meta"))
        tartType = header["type"]
        numberOfPositions = header["numberOfPositions"]
        numberOfFrames = header["numberOfFrames"]
        numberOfPallets = header["numberOfPallets"]

        pallets = []
        surfaces = []
        metaDatas = []

        nameTemplate = "%d-%d.%s"

        for positionIndex in range(numberOfPositions):
            for frameIndex in range(numberOfFrames):

                surfaceName = nameTemplate % (positionIndex, frameIndex, "png")
                surface = pygame.image.load(tartFile.extractfile(surfaceName))
                surfaces.append(surface)

                metaDataName = nameTemplate % (positionIndex, frameIndex, "meta")
                metaDataDict = ReadMetaData(tartFile.extractfile(metaDataName))
                metaData = MetaData(metaDataDict)
                metaDatas.append(metaData)

        for palletIndex in range(numberOfPallets) :

            palletName = "%d.lut" % palletIndex
            palletBuffer = tartFile.extractfile(palletName).read()
            pallet = palletPixelReader.unpack_from(palletBuffer)

            pallets.append(pallet)

    return TartData(tartType, pallets, surfaces, metaDatas, numberOfPositions, numberOfFrames)

def ReadMetaData(metaDataFile):

    keyAndStrValue = map(lambda x: x.strip().split("="), metaDataFile.readlines())
    keyAndValue = map(lambda x: (x[0], int(x[1])), keyAndStrValue)

    return dict(keyAndValue)
