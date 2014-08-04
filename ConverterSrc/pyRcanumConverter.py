from os import  path
from glob import glob
import os

from ConverterSrc.Converters.BikConvert import BikConverter


extensionToConverter = {}


def ConvertFiles(basePath, removeOriginal):

    for filePath in glob(path.join(basePath, "*")):

        if path.isdir(filePath):

            ConvertFiles(filePath, removeOriginal)

        else:

            ConvertFile(filePath, removeOriginal)

def ConvertFile(filePath,removeOriginal):

    extension = path.splitext(filePath)[1].lower()

    if extension in extensionToConverter:

        converter = extensionToConverter[extension]

        print("Converting: '%s'.." % filePath)
        converter(filePath)

        if removeOriginal:
            os.remove(filePath)