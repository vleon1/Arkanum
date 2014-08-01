from struct import Struct


class ImageInfo:

    reader = Struct("<LLLiiii")

    def __init__(self, inputFile):

        imageInfoData = inputFile.read(ImageInfo.reader.size)

        width, height, self.dataSize, drawOffsetX, drawOffsetY, animationOffsetX, animationOffsetY = ImageInfo.reader.unpack(imageInfoData)

        self.size = (width, height)
        self.drawOffset = (drawOffsetX, drawOffsetY)
        self.animationOffset = (animationOffsetX, animationOffsetY)
