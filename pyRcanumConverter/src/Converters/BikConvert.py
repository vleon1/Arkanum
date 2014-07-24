import subprocess

commandTemplate = r"ffmpeg -i %s -vcodec mpeg1video -acodec libmp3lame -intra -r 24 -vb 20M %s"

def BikConverter(inputFilePath):

    outputFilePath = inputFilePath.replace(".bik", ".mpg")

    command = commandTemplate % (inputFilePath, outputFilePath)

    subprocess.check_call(command)