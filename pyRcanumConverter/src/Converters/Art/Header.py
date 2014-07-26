from struct import Struct

import ArtType


headerReader = Struct("<" + ("L" * 33))


def Read(inputFile):

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

    if artType == ArtType.ROTATING_ART or artType == ArtType.MOVING_ART:
        numberOfPositions = 8
        numberOfFrames = header[8]
    else:
        numberOfPositions = header[8]
        numberOfFrames = 1

    return artType, numberOfPallets, numberOfPositions, numberOfFrames
