from struct import Struct

from ConverterSrc.Converters.Art import ArtType


headerReader = Struct("<" + ("L" * 33))


# Header long[33]
# [0] = type
# [1] = ?? most values are 8 but not all
# [2] = always 8
# [3] = ??
# [4:7] = for each field that is not 0 additional pallet is present, but the values differ.
#         my guess that each of those fields is actually an rgb color with byte padding at the end.
# [8] = some kind of elevation maybe?
# [9] = number of frames per angle. (type 0 and 2 have 8 angles, or others have 1)
# [10:34] = ??

def Read(inputFile):

    headerData = inputFile.read(headerReader.size)
    header = headerReader.unpack(headerData)

    artType = header[0]

    numberOfPallets = 1
    if header[6] != 0:
        numberOfPallets += 1
    if header[5] != 0:
        numberOfPallets += 1
    if header[4] != 0:
        numberOfPallets += 1

    if artType == ArtType.ROTATING_ART or artType == ArtType.MOVING_ART:
        numberOfPositions = 8
        numberOfFrames = header[8]
    else:
        numberOfPositions = header[8]
        numberOfFrames = 1

    return artType, numberOfPallets, numberOfPositions, numberOfFrames
