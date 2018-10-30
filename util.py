def runBashCommand(command):
    return os.popen(command).read()

def writeToMakefile(fileContents):
    makefile = open("Makefile", 'w')
    makefile.write(fileContents)
    makefile.close()