from cStringIO import StringIO
import pygame

from EngineSrc.DataTypes.Art import Pallet, ImageInfo, Header, Image


class Art(object):

    def __init__(self, header, pallets, imageInfos, imageDatas):

        self.header = header

        self.pallets = pallets

        self.imageInfos = imageInfos
        self.imageDatas = imageDatas

    def GetImage(self, palletIndex, positionIndex, frameIndex):

        imageData = self.imageDatas[positionIndex * self.header.numberOfFrames + frameIndex]
        imageInfo = self.imageInfos[positionIndex * self.header.numberOfFrames + frameIndex]
        pallet = self.pallets[palletIndex]

        imageBase = StringIO()
        for pixel in imageData:
            imageBase.write(pallet[ord(pixel)])

        return pygame.image.fromstring(imageBase.getvalue(), imageInfo.size, "RGBA").convert_alpha(), imageInfo

def Read(inputFilePath):

    with open(inputFilePath, "rb") as inputFile:

        header = Header.Read(inputFile)

        pallets = map(lambda i: Pallet.Read(inputFile), range(header.numberOfPallets))

        imageInfos = map(lambda i: ImageInfo.Read(inputFile), range(header.numberOfPositions * header.numberOfFrames))
        imageDatas = map(lambda imageInfo: Image.Read(inputFile, imageInfo), imageInfos)

    return Art(header, pallets, imageInfos, imageDatas)