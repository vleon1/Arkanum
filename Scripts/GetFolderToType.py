from glob import glob
from os import path

from struct import Struct

typeReader = Struct("<" + ("xxxx" * 7) + "L")

def ReadFolder(folderPath):

    types = []

    for filePath in glob(path.join(folderPath, "*")):
    
        if path.isdir(filePath):
            types.extend(ReadFolder(filePath))
            
        elif filePath.lower().endswith(".art"):
            with open(filePath, "rb") as artFile:
                typeData = artFile.read(typeReader.size)
            types.append(typeReader.unpack(typeData)[0])
        
    return types

folderToTypes = {}

for folderPath in glob("*"):
    if path.isdir(folderPath):
        folderToTypes[folderPath] = ",".join([str(i) for i in list(set(ReadFolder(folderPath)))])
        
for folder in folderToTypes:

    print("%s: %s" % (folder, folderToTypes[folder]))