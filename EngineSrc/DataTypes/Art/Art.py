from cStringIO import StringIO
import pygame

from EngineSrc.DataTypes.Art import Pallet, ImageInfo, Header, Image


class Art(object):

    def __init__(self, header, pallets, imageInfos, imageDatas):

        self.header = header

        self.pallets = pallets

        self.imageInfos = imageInfos
        self.imageDatas = imageDatas

        self.images = map(lambda x: map(lambda y: None, self.pallets), self.imageInfos)

    def GetImage(self, palletIndex, positionIndex, frameIndex):

        image = self.images[positionIndex * self.header.numberOfFrames + frameIndex][palletIndex]

        if image:
            return image

        imageData = self.imageDatas[positionIndex * self.header.numberOfFrames + frameIndex]
        imageInfo = self.imageInfos[positionIndex * self.header.numberOfFrames + frameIndex]
        pallet = self.pallets[palletIndex]

        imageBase = StringIO()
        for pixel in imageData:
            imageBase.write(pallet[ord(pixel)])

        image = pygame.image.fromstring(imageBase.getvalue(), imageInfo.size, "RGBA").convert_alpha()
        self.images[positionIndex * self.header.numberOfFrames + frameIndex][palletIndex] = image
        return image

def Read(inputFilePath):

    with open(inputFilePath, "rb") as inputFile:

        header = Header.Read(inputFile)

        pallets = map(lambda i: Pallet.Read(inputFile), range(header.numberOfPallets))

        imageInfos = map(lambda i: ImageInfo.Read(inputFile), range(header.numberOfPositions * header.numberOfFrames))
        imageDatas = map(lambda imageInfo: Image.Read(inputFile, imageInfo), imageInfos)

    return Art(header, pallets, imageInfos, imageDatas)