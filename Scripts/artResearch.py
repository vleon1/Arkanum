from glob import glob
from os import path

from struct import Struct

def ReadFolder(folderPath):

    types = []

    for filePath in glob(path.join(folderPath, "*")):
    
        if path.isdir(filePath):
            ReadFolder(filePath)
            
        elif filePath.lower().endswith(".art"):
            
            if ReadNumberOfImagesMinus1(filePath) !=  7:
                print(filePath)
                
def ReadType(filePath):
    reader = Struct("<L")
    with open(filePath, "rb") as artFile:
        data = artFile.read(reader.size)
    return reader.unpack(data)[0]
    
def Read8Value(filePath):
    reader = Struct("<xxxxL")
    with open(filePath, "rb") as artFile:
        data = artFile.read(reader.size)
    return reader.unpack(data)[0]
    
def ReadPallets(filePath):
    reader = Struct("<LLLLLLL")
    with open(filePath, "rb") as artFile:
        data = reader.unpack(artFile.read(reader.size))
    if data[6] != 0:
        return 4
    elif data[5] != 0:
        return 3
    elif data[4] != 0:
        return 2
    else:
        return 1

def ReadNumberOfImagesMinus1(filePath):

    reader = Struct("<" + "xxxx" * 7 + "L")
    with open(filePath, "rb") as artFile:
        return reader.unpack(artFile.read(reader.size))[0]
		
def ReadNumberOfImages(filePath):

    reader = Struct("<" + "xxxx" * 8 + "L")
    with open(filePath, "rb") as artFile:
        return reader.unpack(artFile.read(reader.size))[0]

for folderPath in glob("*"):
    if path.isdir(folderPath):
        ReadFolder(folderPath)
