from cStringIO import StringIO
import pygame


class Image(object):

    def __init__(self, inputFile, info, pallet):

        self.info = info
        self.pallet = pallet

        self.texture = None

        imageFinalDataSize = self.info.size[0] * self.info.size[1]
        isRLE = (self.info.dataSize != imageFinalDataSize)

        self.data = Image.ReadRleData(inputFile, self.info) if isRLE else inputFile.read(imageFinalDataSize)

    def Texture(self):

        if not self.texture:

            baseTexture = pygame.image.fromstring(self.data, self.info.size, "P")
            baseTexture.set_colorkey(self.pallet.alphaColor)
            baseTexture.set_palette(self.pallet.data)

            self.texture = baseTexture.convert()

        return self.texture

    def Render(self, baseTexture, position):

        baseTexture.blit(self.Texture(), position)

    @staticmethod
    def ReadRleData(inputFile, imageInfo):

        dataStream = StringIO()

        dataRead = 0

        while dataRead < imageInfo.dataSize:

            rleByte = ord(inputFile.read(1))
            dataRead += 1

            isNextByteRepeating = (rleByte & 0x80) == 0
            repeatAmount = rleByte & 0x7F

            if isNextByteRepeating:

                nextByte = inputFile.read(1)
                dataRead += 1

                data = nextByte * repeatAmount

            else:

                data = inputFile.read(repeatAmount)
                dataRead += repeatAmount

            dataStream.write(data)

        return dataStream.getvalue()
