from ConverterSrc.Converters.Art import ArtData


def ArtConverter(inputFilePath):

    imageData = ArtData.ReadArtData(inputFilePath)

    outputFilePath = inputFilePath.lower().replace(".art", ".tart")

    imageData.Write(outputFilePath)

