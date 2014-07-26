import subprocess
import os
from os import path
from tempfile import TemporaryFile

commandTemplate = r"ffmpeg -i %s -vcodec mpeg1video -acodec libmp3lame -intra -r 24 -vb 20M %s"

def BikConverter(inputFilePath):

    outputFilePath = inputFilePath.replace(".bik", ".mpg")
    if path.exists(outputFilePath):
        os.remove(outputFilePath)

    command = commandTemplate % (inputFilePath, outputFilePath)

    with TemporaryFile() as logFile:
        subprocess.check_call(command,
                              stdout = logFile, stderr = subprocess.STDOUT)
