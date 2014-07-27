from glob import glob
from os import path

def Extensions(folder):

    extensions = []
    
    for filePath in glob(path.join(folder, "*")):
    
        if path.isdir(filePath):
        
            extensions.extend(Extensions(filePath))
            
        else:
        
            extension = path.splitext(filePath)[1].lower()
            extensions.append(extension)
            
    return extensions

def FindFolderContaining(folder, extension):

    for filePath in glob(path.join(folder, "*")):
    
        if path.isdir(filePath):
        
            candidate = FindFolderContaining(filePath, extension)
            
            if candidate is not None:
            
                return candidate
            
        else:
        
            if path.splitext(filePath)[1].lower() == extension:
            
                return filePath

    return None
    
startDir = r"D:\Work\Arcanum\GameData\WipArcanum"

extensions = list(set(Extensions(startDir)))

extensionToFolder = {}

for extension in extensions:
    
    fullPath = FindFolderContaining(startDir, extension)
    
    extensionToFolder[extension] = path.relpath(fullPath, startDir)
    
for key in extensionToFolder:

    print("[[%s]]: example='%s'" % (key, extensionToFolder[key]))
    