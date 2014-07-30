from EngineSrc.DataTypes.Art import Art


def LoadAngledAnimation(artFilePath, palletIndex, positionIndex, frameIndex):

    art = Art.Read(artFilePath)

    image, imageInfo = art.GetImage(palletIndex, positionIndex, frameIndex)

    return image

def LoadAnimation(artFilePath, palletIndex, frameIndex):

    return LoadAngledAnimation(artFilePath, palletIndex, 0, frameIndex)

def LoadSingle(artFilePath, palletIndex):

    return LoadAnimation(artFilePath, palletIndex, 0)
