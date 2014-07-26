import sys
import os
from os import path

from src import pyRcanumConverter

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("Usage: %s {basePath}" % sys.argv[0])
        print("")
        print("basePath = The root path of arcanum data to convert.")
        print("")

        sys.exit(1)

    appDirectory = path.dirname(sys.argv[0])
    toolsDirectory = path.join(appDirectory, "tools")
    paths = os.getenv("path")
    paths = (paths + os.pathsep + toolsDirectory) if paths else toolsDirectory
    os.putenv("path", paths)

    basePath = sys.argv[1]

    pyRcanumConverter.ConvertFiles(basePath, removeOriginal = True)
