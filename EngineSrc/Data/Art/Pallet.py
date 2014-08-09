from struct import Struct

class Pallet(object):

    reader = Struct("<BBBx")

    def __init__(self, inputFile):

        self.data = [None] * 256

        self.data[0] = Pallet.ReadPalletPixel(inputFile, alpha = 0)
        for i in range(1, 256):
            self.data[i] = Pallet.ReadPalletPixel(inputFile, alpha = 255)

    @staticmethod
    def ReadPalletPixel(inputFile, alpha):

        palletPixelData = inputFile.read(Pallet.reader.size)

        blue, green, red = Pallet.reader.unpack(palletPixelData)

        return red, green, blue, alpha
