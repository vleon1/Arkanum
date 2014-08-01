class Mes(object):

    def __init__(self, lines):
        self.lines = lines

def Read(inputFilePath):

    with open(inputFilePath, "rb") as inputFile:

        data = inputFile.read()

    lineNumbersAndData = []
    maxLineNumber = 0

    startIndex = 0
    while True:

        lineNumber, startIndex = GetLineNumber(data, startIndex)
        if startIndex == -1:
            break

        if lineNumber > maxLineNumber:
            maxLineNumber = lineNumber

        lineData, startIndex = GetLineData(data, startIndex)
        if startIndex == -1:
            break

        lineNumbersAndData.append((lineNumber, lineData))

    lines = [""] * (maxLineNumber + 1)

    for lineNumberAndData in lineNumbersAndData:
        lines[lineNumberAndData[0]] = lineNumberAndData[1]

    return Mes(lines)

def GetLineNumber(data, startIndex):

    lineNumberString, startIndex = GetNextBracketData(data, startIndex)

    return int(lineNumberString), startIndex

def GetLineData(data, startIndex):

    return GetNextBracketData(data, startIndex)

def GetNextBracketData(data, startIndex):

    startBracketIndex = data.find("{", startIndex)
    if startBracketIndex == -1:
        return "-1", -1

    endBracketIndex = data.find("}", startBracketIndex + 1)
    if endBracketIndex == -1:
        return "0", -1

    return data[startBracketIndex + 1: endBracketIndex], endBracketIndex + 1
