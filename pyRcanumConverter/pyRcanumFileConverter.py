import sys
import os
from os import path

from src import pyRcanumConverter

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("Usage: %s {filePath}" % sys.argv[0])
        print("")
        print("filePath = The file to convert.")
        print("")

        sys.exit(1)

    appDirectory = path.dirname(sys.argv[0])
    toolsDirectory = path.join(appDirectory, "tools")
    paths = os.getenv("path")
    paths = (paths + os.pathsep + toolsDirectory) if paths else toolsDirectory
    os.putenv("path", paths)

    filePath = sys.argv[1]

    pyRcanumConverter.ConvertFile(filePath, removeOriginal = False)
