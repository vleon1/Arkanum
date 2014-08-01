import pygame

import Type
from Header import Header
from Pallet import Pallet
from ImageInfo import ImageInfo
from Image import Image

class Art(object):

    def __init__(self, inputFile, header):

        self.header = header

        self.pallets = map(lambda i: Pallet(inputFile), range(self.header.numberOfPallets))

        infos = map(lambda i: ImageInfo(inputFile), range(self.header.numberOfAngles * self.header.numberOfFrames))

        self.images = map(lambda imageInfo:
                            map(lambda pallet: Image(inputFile, imageInfo, pallet), self.pallets),
                          infos)

    def Image(self, angleIndex, frameIndex = 0, palletIndex = 0):
        return self.images[angleIndex * self.header.numberOfFrames + frameIndex][palletIndex]

class RotatingAnimationArt(Art):

    def __init__(self, inputFile, header):
        super(RotatingAnimationArt, self).__init__(inputFile, header)

class StaticArt(Art):

    def __init__(self, inputFile, header):
        super(StaticArt, self).__init__(inputFile, header)

    def Image(self, frameIndex = 0, palletIndex = 0):
        return self.images[frameIndex][palletIndex]

class FontArt(StaticArt):

    ART_ASCII_OFFSET = 31

    def __init__(self, inputFile, header):
        super(FontArt, self).__init__(inputFile, header)

    def Sentence(self, sentence):

        characterImages = map(lambda character: self.Image(ord(character) - FontArt.ART_ASCII_OFFSET), sentence)

        totalWidth = sum(map(lambda x: x.info.drawOffset[0], characterImages))
        totalHeight = characterImages[1].info.drawOffset[1]

        sentenceTexture = pygame.Surface((totalWidth, totalHeight))
        sentenceTexture.set_colorkey((0, 0, 0))

        currentPosition = [0 , 0]
        for characterImage in characterImages:

            characterImage.Render(sentenceTexture, currentPosition)

            currentPosition[0] += characterImage.info.drawOffset[0]

        return sentenceTexture

def Read(inputFilePath):

    with open(inputFilePath, "rb") as inputFile:

        header = Header(inputFile)

        if header.type == Type.ROTATING_ART or header.type == Type.MOVING_ART:

            return RotatingAnimationArt(inputFile, header)

        elif header.type == Type.FONT_ART:

            return FontArt(inputFile, header)

        else:

            return StaticArt(inputFile, header)
