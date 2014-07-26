from cStringIO import StringIO
from struct import Struct


palletPixelReader = Struct("<BBBx")
palletPixelWriter = Struct("<BBB")

def Read(inputFile):

    pallet = StringIO()

    for i in range(256):
        pallet.write(ReadPalletPixel(inputFile))

    return pallet

def ReadPalletPixel(inputFile):

    palletPixelData = inputFile.read(palletPixelReader.size)

    blue, green, red = palletPixelReader.unpack(palletPixelData)

    return palletPixelWriter.pack(red, green, blue)
