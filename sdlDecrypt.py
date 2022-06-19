#! python3

import re
import sys
import os
import traceback


logRegex = re.compile(r"""(\s*(\w*)\s(\w*)\s(\w*)\s(\w*)\s(\w*)\s(\w*)\s*$)""", re.VERBOSE | re.MULTILINE)
keyRegex = re.compile(r"""(\s*(\w*)\s?=\s?(\.*)$)""", re.VERBOSE)

# Provides Raw String to be Parsed
def readFileInput(fileName):
    print("Log input called")
    try:
        logFile = open(os.path.join('.','sources', fileName), encoding='utf-8')
        print("Successfully read file")
        return logFile.read()
    except:
        print("Error while reading file")
        return ''


#All of that stuff is very overkill for the actual function of this script, which is search and replace from Key.
logList = list()
distinctEntities = list()

def addIfDistinct(identifier):
    print("Identifier : " + identifier)
    if identifier not in distinctEntities:
        print("New identifier found. Adding " + identifier + " to the entity list.")
        distinctEntities.append(identifier)

def parseLog(logInput):
    try:
        matchList = logRegex.findall(logInput)
    except:
        print("parseLogDictionary: Error in regex parser.")

    #print(str(len(matchList)))
    for match in matchList:
        logList.append(match[0])
        identifier = match[3]
        addIfDistinct(identifier)
        identifier = match[5]
        addIfDistinct(identifier)

def parseKey(keyInput):
    hashDict = dict()
    try:
        matchList = keyRegex.findall(keyInput)
    except:
        print("parseKey: Error in regex parser.")

    for match in matchList:
        hashDict[match[1]] = match[2]

    return hashDict


def clearLog(log, hashDict):
    clearedLog = log
    for hash in hashDict.keys():
        clearedLog = clearedLog.replace(hash, hashDict[hash])
    return clearedLog

def writeStringToFile(string, outputFileName):
    try:
        os.mkdir(os.path.join('.','output'))
        print("Could not find output directory, creating the output directory.")
    except:
        print("Directory 'output' already present.")

    try:
        resultFile = open(os.path.join('.','output', outputFileName), 'w', encoding='utf-8')

        resultFile.write(string)

        resultFile.close()
        print("Wrote to file successfully")
    except:
        print("writeStringToFile: Could not write result")
        traceback.print_exc()


#file string.
log = readFileInput(str(sys.argv[1]))

#key string.
key = readFileInput(str(sys.argv[2]))

writeStringToFile(clearLog(log, parseKey(key)), "clearedLogFromKey.txt")





