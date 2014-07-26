from cStringIO import StringIO
from struct import Struct

from PIL import Image

class ArtData(object):


    def __init__(self, artType, pallets, images, numberOfPositions, numberOfFrames):

        self.artType = artType

        self.pallets = pallets
        self.images = images

        self.numberOfPositions = numberOfPositions
        self.numberOfFrames = numberOfFrames

    def GetImage(self, position, frame):

        return self.images[position * self.numberOfFrames + frame]


# Art types
ROTATING_ART = 0
STATIC_ART = 1
MOVING_ART = 2

FONT_ART = 5

FACADE_ART = 9 # Am i sure?
MAGIC_ART = 11 # Am i sure?
# Any other??


def ArtConverter(inputFilePath):

    with open(inputFilePath, "rb") as inputFile:

        artType, numberOfPallets, numberOfPositions, numberOfFrames = ReadHeader(inputFile)

        pallets = map(lambda i: ReadPallet(inputFile), range(numberOfPallets))

        numberOfImages = numberOfPositions * numberOfFrames

        imageInfos = map(lambda i: ReadImageInfo(inputFile), range(numberOfImages))

        images = map(lambda imageInfo: ReadImage(inputFile, imageInfo), imageInfos)

    outputImageFilePathTemplate = inputFilePath.lower().replace(".art", "_%d_%d_%d.png")
    outputMetaDataFilePathTemplate = outputImageFilePathTemplate.replace(".png", ".meta")

    for positionIndex in range(numberOfPositions):

        for frameIndex in range(numberOfFrames):

            for palletIndex in range(numberOfPallets) :

                image = images[positionIndex * numberOfFrames + frameIndex].copy()
                imageInfo = imageInfos[positionIndex * numberOfFrames + frameIndex]

                pallet = pallets[palletIndex]

                image.putpalette(pallet)

                outputImageFilePath = outputImageFilePathTemplate % (positionIndex, frameIndex, palletIndex)
                outputMetaDataFilePath = outputMetaDataFilePathTemplate % (positionIndex, frameIndex, palletIndex)

                image.save(outputImageFilePath)
                imageInfo.Save(outputMetaDataFilePath)

headerReader = Struct("<" + ("L" * 33))
def ReadHeader(inputFile):

    headerData = inputFile.read(headerReader.size)
    header = headerReader.unpack(headerData)

    artType = header[0]

    if header[6] != 0:
        numberOfPallets = 4
    elif header[5] != 0:
        numberOfPallets = 3
    elif header[4] != 0:
        numberOfPallets = 2
    else:
        numberOfPallets = 1

    if artType == ROTATING_ART or artType == MOVING_ART:
        numberOfPositions = 8
        numberOfFrames = header[8]
    else:
        numberOfPositions = header[8]
        numberOfFrames = 1

    return artType, numberOfPallets, numberOfPositions, numberOfFrames


def ReadPallet(inputFile):

    palletPixels = []

    for i in range(256):
        palletPixels.extend(ReadPalletPixel(inputFile))

    return palletPixels

palletPixelReader = Struct("<BBBx")
def ReadPalletPixel(inputFile):

    palletPixelData = inputFile.read(palletPixelReader.size)

    blue, green, red = palletPixelReader.unpack(palletPixelData)

    return red, green, blue

class ImageInfo:

    def __init__(self, size, dataSize, x, y, dX, dY):

        self.size = size

        self.dataSize = dataSize

        self.x = x
        self.y = y

        self.dX = dX
        self.dY = dY

        self.isRLE = (dataSize != size[0] * size[1])

    def Save(self, outputFilePath):

        with open(outputFilePath, "w") as outputFile:

            outputFile.write("x=%s\n" % self.x)
            outputFile.write("y=%s\n" % self.y)
            outputFile.write("dX=%s\n" % self.dX)
            outputFile.write("dY=%s" % self.dY)

imageInfoReader = Struct("<LLLiiii")
def ReadImageInfo(inputFile):

    imageInfoData = inputFile.read(imageInfoReader.size)

    width, height, dataSize, x, y, dX, dY = imageInfoReader.unpack(imageInfoData)
    size = (width, height)

    imageInfo = ImageInfo(size, dataSize, x, y, dX, dY)

    return imageInfo


def ReadImage(inputFile, imageInfo):

    imageData = ReadRleData(inputFile, imageInfo) if imageInfo.isRLE else inputFile.read(imageInfo.size[0] * imageInfo.size[1])

    image = Image.frombytes("L", imageInfo.size, imageData)

    return image

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
