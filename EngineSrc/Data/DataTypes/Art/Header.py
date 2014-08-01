from struct import Struct

# Header long[33]
# [0] = type (flags)
# [1] = fps
# [2] = always 8 # number of angels when art is rotating?
# [3:7] = for each field that is not 0 additional pallet is present, but the values sometimes differ.
#         my guess that each of those fields is actually an rgb color with byte padding at the end.
# [7] = action frame?
# [8] = number of frames per angle. (type 0 and 2 have 8 angles, or others have 1)
# [9:33] = ??
from EngineSrc.Data.DataTypes.Art import Type


class Header(object):

    reader = Struct("<LLxxxxLLLLLL" +("xxxx" * 24))

    def __init__(self, inputFile):

        headerData = inputFile.read(Header.reader.size)
        self.type, self.fps, pallet1, pallet2, pallet3, pallet4, self.actionFrame, framesPerAngle = Header.reader.unpack(headerData)

        self.numberOfPallets = bool(pallet1) + bool(pallet2) + bool(pallet3) + bool(pallet4)

        if self.type == Type.ROTATING_ART or self.type == Type.MOVING_ART:
            self.numberOfAngles = 8
            self.numberOfFrames = framesPerAngle
        else:
            self.numberOfAngles = 1
            self.numberOfFrames = framesPerAngle
