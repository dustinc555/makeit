#!/usr/bin/env python

# Inspiration driven from: https://github.com/Melinysh/PyMake
# which falls under: The MIT License (MIT) Copyright (c) 2018 Stephen Melinyshyn
import os, glob
from os import listdir
import argparse
import subprocess
from ConfigParser import SafeConfigParser




def getArguments(contents):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="The working directory, if blank uses current directory.")
    parser.add_argument("--flags", help="Compilation flags. If left blank uses: .")
    args = parser.parse_args()

    contents['directory'] = args.dir if args.dir else os.getcwd()
    contents['flags'] = args.flags if args.flags else "-Wall -O3 -std=c++11 $(INC)"

def generateMakefile(contents):
    fileContents = ""

    files = list((f for f in listdir(contents['directory']) if f.endswith('.cpp')))
    if len(files) == 0:
        raise RuntimeError("No cpp source files.")

    mainFile = ""
    numberOfMains = 0
    for file in files:
        if runBashCommand('grep -i ' + '"int main()" ' + file).strip() == "int main()":
            mainFile = file.split('.')[0]
            numberOfMains += 1
    if numberOfMains > 1:
        print('Multiple main functions detected.\nThe program may not run correctly.')
    elif numberOfMains == 0:
        print("There is no main function.")
    filesiter = iter(files)
    fileContents += 'SOURCE = '
    fileContents += next(filesiter) + " \\\n"
    for file in filesiter:
        fileContents += "   " + file + " \\\n"
    fileContents += "\nOBJS = $(SOURCE:.cpp=.o)\n\n"
    fileContents += "#GNU C/C++ Compiler\n"
    fileContents += "GCC = g++\n\n"
    fileContents += "#GNU C/C++ Linker\n"
    fileContents += "LINK = g++\n\n"
    fileContents += "# Compiler flags\n"
    fileContents += "INC = \n"
    fileContents += "CFLAGS = " + contents["flags"] + "\n"
    fileContents += "CXXFLAGS = $(CFLAGS)\n\n"
    fileContents += "# Fill in special libraries needed here\n"
    fileContents += "LIBS =\n\n"
    fileContents += ".PHONY: clean\n\n"
    fileContents += "# Targets include all, clean, debug, tar\n\n"
    fileContents += "all : " + mainFile + "\n\n"
    fileContents += mainFile + ': $(OBJS)\n'
    fileContents += "	$(LINK) -o $@ $^ $(LIBS)\n\n"
    fileContents += "clean:\n"
    fileContents += "	rm -rf *.o *.d core " + mainFile + "\n\n"
    fileContents += "debug: CXXFLAGS = -DDEBUG -g -std=c++11\n"
    fileContents += "debug: " + mainFile + "\n\n"
    fileContents += "tar: clean\n"
    fileContents += "	tar zcvf " + mainFile + ".tgz $(SOURCE) *.h Makefile\n"
    fileContents += "help:\n"
    fileContents += '	@echo "	make gas  - same as make all"\n'
    fileContents += '	@echo "	make all   - builds the main target"\n'
    fileContents += '	@echo "	make       - same as make all"\n'
    fileContents += '	@echo "	make clean - remove .o .d core gas"\n'
    fileContents += '	@echo "	make debug - make all with -g and -DDEBUG"\n'
    fileContents += '	@echo "	make tar   - make a tarball of .cpp and .h files"\n'
    fileContents += '	@echo "	make help  - this message"\n\n'
    fileContents += "-include $(SOURCE:.cpp=.d)\n\n"
    fileContents += '%.d: %.cpp\n'
    fileContents += '	@set -e; /usr/bin/rm -rf $@;$(GCC) -MM $< $(CXXFLAGS) > $@'
    return fileContents

def runBashCommand(command):
    return os.popen(command).read()

def writeToMakefile(fileContents):
    makefile = open("Makefile", 'w')
    makefile.write(fileContents)
    makefile.close()

def start():
    contents = {}
    getArguments(contents)
    MakeFile = generateMakefile(contents)
    writeToMakefile(MakeFile)
    exit(0)

start()
