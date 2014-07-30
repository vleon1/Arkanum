from cStringIO import StringIO


def Read(inputFile, imageInfo):

    isRLE = (imageInfo.dataSize != imageInfo.size[0] * imageInfo.size[1])

    imageData = ReadRleData(inputFile, imageInfo) if isRLE else inputFile.read(imageInfo.size[0] * imageInfo.size[1])

    return imageData

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

