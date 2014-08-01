from struct import Struct

class Pallet(object):

    reader = Struct("<BBBx")

    def __init__(self, inputFile):

        self.data = [None] * 256
        for i in range(0, 256):
            self.data[i] = Pallet.ReadPalletPixel(inputFile)

        self.alphaColor = self.data[0]

    @staticmethod
    def ReadPalletPixel(inputFile):

        palletPixelData = inputFile.read(Pallet.reader.size)

        blue, green, red = Pallet.reader.unpack(palletPixelData)

        return red, green, blue
