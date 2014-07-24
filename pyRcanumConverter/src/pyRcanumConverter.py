from os import  path
from glob import glob

from Converters.BikConvert import BikConverter


extensionToConverter = {".bik" : BikConverter}


def Convert(basePath):

    for filePath in glob(path.join(basePath, "*")):

        if path.isdir(filePath):

            Convert(filePath)

        else:

            extension = path.splitext(filePath)[1]

            if extension in extensionToConverter:

                converter = extensionToConverter[extension]

                converter(filePath)
