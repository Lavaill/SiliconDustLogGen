#! python3

import re
import sys
import os
import traceback
import random
import string


logRegex = re.compile(r"""(\s*(\w*)\s(\w*)\s(\w*)\s(\w*)\s(\w*)\s(\w*)\s*$)""", re.VERBOSE | re.MULTILINE)

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

def random_string(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))

distinctHashes = list()


def random_distinct_string(length):
    string = random_string
    if distinctHashes.contains(string):
        return random_distinct_string(length)
    else:
        distinctHashes.append(string)
        return string

def addIfDistinct(identifier, distinctEntities):
    print("Identifier : " + identifier)
    if identifier not in distinctEntities:
        print("New identifier found. Adding " + identifier + " to the entity list.")
        distinctEntities.append(identifier)

def getDistinctEntities(logInput):
    distinctEntities = list()
    try:
        matchList = logRegex.findall(logInput)
    except:
        print("parseLogDictionary: Error in regex parser.")

    #print(str(len(matchList)))
    for match in matchList:
        identifier = match[2]
        addIfDistinct(identifier, distinctEntities)
        identifier = match[4]
        addIfDistinct(identifier, distinctEntities)

    return distinctEntities


def generateKeyDict(entities):
    keyDict = dict()

    for entity in entities:
        keyDict[entity] = random_distinct_string(8)

    return keyDict

def hashLog(log, keyDict):
    hashedLog = log
    for entity in keyDict.keys():
        hashedLog = hashedLog.replace(entity, keyDict[entity])
    return hashedLog

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

def writeDictionaryToFile(dictionary, outputFileName):
    try:
        os.mkdir(os.path.join('.','output'))
        print("Could not find output directory, creating the output directory.")
    except:
        print("Directory 'output' already present.")

    try:
        resultFile = open(os.path.join('.','output', outputFileName), 'w', encoding='utf-8')

        for key in dictionary.keys():
            resultFile.write(str(key) + " = " + dictionary[key] )
        

        resultFile.close()
        print("Wrote to file successfully")
    except:
        print("writeDictionaryToFile: Could not write result")
        traceback.print_exc()


#file string.
log = readFileInput(str(sys.argv[1]))

#generate key
key = generateKeyDict(getDistinctEntities(log))

writeStringToFile(hashLog(log, key), "hashedLog.txt")
writeDictionaryToFile(key, "key.txt")





