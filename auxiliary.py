import strings


def logMessage(short_message, message):
    print(short_message)
    print(message)


def showHelp():
    logMessage("Usage:", strings.STRS['HELP'])
