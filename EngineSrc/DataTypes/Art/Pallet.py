from struct import Struct


palletPixelReader = Struct("<BBBx")
palletPixelWriter = Struct("<BBBB")

def Read(inputFile):

    inputFile.read(palletPixelReader.size)
    pallet = [palletPixelWriter.pack(0, 0, 0, 0)]
    for i in range(1, 256):
        pallet.append(ReadPalletPixel(inputFile))

    return pallet

def ReadPalletPixel(inputFile):

    palletPixelData = inputFile.read(palletPixelReader.size)

    blue, green, red = palletPixelReader.unpack(palletPixelData)

    return palletPixelWriter.pack(red, green, blue, 255) # alpha is 255 by default.
