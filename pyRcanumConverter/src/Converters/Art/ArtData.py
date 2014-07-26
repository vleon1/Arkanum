import os

import tarfile

import Header
import Pallet
import ImageInfo
import Image

class ArtData(object):

    def __init__(self, artType, pallets, images, imageInfos, numberOfPositions, numberOfFrames):

        self.type = artType

        self.pallets = pallets
        self.images = images
        self.metaDatas = map(lambda x: x.SaveMetaData(), imageInfos)

        self.numberOfPositions = numberOfPositions
        self.numberOfFrames = numberOfFrames

    def GetImage(self, positionIndex, frameIndex):

        return self.images[positionIndex * self.numberOfFrames + frameIndex]

    def GetMetaData(self, positionIndex, frameIndex):

        return self.metaDatas[positionIndex * self.numberOfFrames + frameIndex]

    def Write(self, outputFilePath):

        with tarfile.open(outputFilePath, "w:bz2") as outputFile:

            for positionIndex in range(self.numberOfPositions):
                for frameIndex in range(self.numberOfFrames):

                    image = self.GetImage(positionIndex, frameIndex)
                    metaData = self.GetMetaData(positionIndex, frameIndex)

                    nameTemplate = "%d-%d.%s"

                    imageName = nameTemplate % (positionIndex, frameIndex, "png")
                    metaDataName = nameTemplate % (positionIndex, frameIndex, "meta")

                    AddToTar(outputFile, image, imageName)
                    AddToTar(outputFile, metaData, metaDataName)

            for palletIndex in range(len(self.pallets)) :

                pallet = self.pallets[palletIndex]

                palletName = "%d.lut" % palletIndex

                AddToTar(outputFile, pallet, palletName)

def ReadArtData(inputFilePath):

    with open(inputFilePath, "rb") as inputFile:

        artType, numberOfPallets, numberOfPositions, numberOfFrames = Header.Read(inputFile)

        pallets = map(lambda i: Pallet.Read(inputFile), range(numberOfPallets))

        imageInfos = map(lambda i: ImageInfo.Read(inputFile), range(numberOfPositions * numberOfFrames))

        images = map(lambda imageInfo: Image.Read(inputFile, imageInfo), imageInfos)

    return ArtData(artType, pallets, images, imageInfos, numberOfPositions, numberOfFrames)

def AddToTar(tarFile, fileObject, fileName):

    tarInfo = tarfile.TarInfo(name = fileName)
    tarInfo.size = GetFileSize(fileObject)

    tarFile.addfile(tarInfo, fileobj = fileObject)

def GetFileSize(fileObject):

    fileObject.seek(0, os.SEEK_END)
    size = fileObject.tell()
    fileObject.seek(0, os.SEEK_SET)

    return size
