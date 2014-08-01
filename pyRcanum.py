import sys
from os import path

from EngineSrc.pyRcanum import Arcanum


if __name__ == "__main__":

    applicationPath = path.dirname(sys.argv[0])
    configPath = sys.argv[1] if len(sys.argv) == 2 else path.join(applicationPath, "pyRcanum.ini")

    arcanum = Arcanum(configPath, applicationPath)
    arcanum.Run()

    sys.exit()
