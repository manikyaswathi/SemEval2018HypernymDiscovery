import re
import sys

# Author : Swathi manikya vallabhajosyula

# input TRAIN|TRIAL file to get line nums of concepts and entities
inputFD = open(sys.argv[1], "r")

# file to separate results
inputFileName = sys.argv[2]
inputFO = open(inputFileName, 'r')

# Concepts file
outputFileNameC = sys.argv[3]
# Entities file
outputFileNameE = sys.argv[4]

outputFOC = open(outputFileNameC,"w")
outputFOE = open(outputFileNameE,"w")

lineCount = 1
countC = 0
countE = 0

ListC = []
ListE = []

for line in inputFD:
    splitline = line.strip().split("\t")
    TarWord = splitline[0]
    TarType = splitline[1]
    matchTypeC = re.compile(r'\b[Cc]oncept\b')
    matchTypeE = re.compile(r'\b[Ee]ntity\b')
    matchedC = re.search(matchTypeC, TarType)
    matchedE = re.search(matchTypeE, TarType)
    if matchedC:
        countC = countC + 1           # line number of concpets
        ListC.append(lineCount)
    elif matchedE:
        countE = countE + 1           # line number of entities
        ListE.append(lineCount)
    lineCount = lineCount + 1

curline = 1
for op in inputFO:
    if curline in ListC:
        outputFOC.write(op)      # writing concpets to concepts file
    elif curline in ListE:
        outputFOE.write(op)      # writing concpets to entities file  
    curline = curline + 1
