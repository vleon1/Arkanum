from struct import Struct

from EngineSrc.DataTypes.Art import Type


headerReader = Struct("<LLxxxxLLLLLL" +("xxxx" * 24))

# Header long[33]
# [0] = type (flags)
# [1] = fps
# [2] = always 8 # number of angels when art is rotating?
# [3:7] = for each field that is not 0 additional pallet is present, but the values sometimes differ.
#         my guess that each of those fields is actually an rgb color with byte padding at the end.
# [7] = action frame?
# [8] = number of frames per angle. (type 0 and 2 have 8 angles, or others have 1)
# [10:34] = ??

class Header(object):

    def __init__(self, artType, fps, numberOfPallets, actionFrame, numberOfPositions, numberOfFrames):

        self.type = artType

        self.fps = fps

        self.numberOfPallets = numberOfPallets

        self.actionFrame = actionFrame

        self.numberOfPositions = numberOfPositions
        self.numberOfFrames = numberOfFrames

def Read(inputFile):

    headerData = inputFile.read(headerReader.size)
    artType, fps, pallet1, pallet2, pallet3, pallet4, actionFrame, framesPerAngle  = headerReader.unpack(headerData)

    numberOfPallets = bool(pallet1) + bool(pallet2) + bool(pallet3) + bool(pallet4)

    if artType == Type.ROTATING_ART or artType == Type.MOVING_ART:
        numberOfPositions = 8
        numberOfFrames = framesPerAngle
    else:
        numberOfPositions = framesPerAngle
        numberOfFrames = 1

    return Header(artType, fps, numberOfPallets, actionFrame, numberOfPositions, numberOfFrames)
