class Config(object):

    pass

def Read(iniFilePath,
         intArguments = (), floatArguments = (), boolArguments = (), listArguments = ()):

    with open(iniFilePath) as iniFile:

        return ParseLines(iniFile.readlines(), 
                          intArguments, floatArguments, boolArguments, listArguments)

def ParseLines(iniLines,
               intArguments = (), floatArguments = (), boolArguments = (), listArguments = ()):

    def RemoveComment(line):

        commentStart = line.find(';')

        return line[:commentStart] if commentStart != -1 else line

    iniLines = list(map(RemoveComment, iniLines))

    iniKeyValues = [x.split("=", 1) for x in iniLines]
    iniKeyValues = [x for x in iniKeyValues if len(x) == 2]
    iniKeyValues = [(x[0].strip(),
                     x[1].strip().strip("\"").strip()) for x in iniKeyValues]

    configDict = dict(iniKeyValues)

    return TranslateConfigDict(configDict,
                               intArguments, floatArguments, boolArguments, listArguments)

def TranslateConfigDict(configDict,
                        intArguments = (), floatArguments = (), boolArguments = (), listArguments = ()):

    for intArgument in intArguments:
        configDict[intArgument] = int(configDict[intArgument])

    for floatArgument in floatArguments:
        configDict[floatArgument] = float(configDict[floatArgument])

    for boolArgument in boolArguments:
        configDict[boolArgument] = bool(configDict[boolArgument])

    for listArgument in listArguments:
            configDict[listArgument] = configDict[listArgument].split(",")

    config = Config()

    list([setattr(config, x, configDict[x]) for x in configDict])

    return config