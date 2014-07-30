from cStringIO import StringIO
from struct import Struct


imageInfoReader = Struct("<LLLiiii")


class ImageInfo:

    def __init__(self, size, dataSize, x, y, dX, dY):

        self.size = size

        self.dataSize = dataSize

        # Center of image or offset relative to tile?
        self.x = x
        self.y = y

        # Offset in animation? or offset relative to tile?
        self.dX = dX
        self.dY = dY

def Read(inputFile):

    imageInfoData = inputFile.read(imageInfoReader.size)

    width, height, dataSize, x, y, dX, dY = imageInfoReader.unpack(imageInfoData)
    size = (width, height)

    imageInfo = ImageInfo(size, dataSize, x, y, dX, dY)

    return imageInfo
