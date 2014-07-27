import sys
from os import path

from EngineSrc.pyRcanum import Arcanum


if __name__ == "__main__":

    srcPath = path.dirname(sys.argv[0])
    dataPath = path.join(srcPath, r"GameData")

    arcanum = Arcanum(dataPath)
    arcanum.Run()

    sys.exit()
