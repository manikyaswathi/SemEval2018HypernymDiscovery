# This program prints Hello, world! SPACE TRIMMING START END, SENTENCES in QAUT$
import re
import nltk
import json
from nltk import word_tokenize
# from collections import defaultdict

print 'Starting the Processing\n'

inputF = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/vocabulary/1A.english.vocabulary.txt","r")
outputF = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/vocabulary/1A.english.vocabulary_0.txt","w")

unigramV = []
bigramV = []
trigramV = []

writeInDump = 'false'

input_vocab = []

singleUn = re.compile(r'(\S+)_(\S+)')
doubleUn = re.compile(r'(\S+)_(\S+)_(\S+)')

for line in inputF:
    lineU = re.sub(r' ', r'_', line)
    lineU = re.sub(r'\n$', r'', lineU)
    lineU = lineU.lower()
    lineU = lineU.lower()
    line = lineU
    mS = re.match(singleUn, lineU)
    mD = re.match(doubleUn, lineU)
    if mD:
        line = re.sub(r'(\S+)_(\S+)_(\S+)', r'\1/ntg \2/ntg \3/ntg', line)
        trigramV.append(line)
    elif mS:
        line = re.sub(r'(\S+)_(\S+)', r'\1/ntg \2/ntg', line)
        bigramV.append(line)
    else:
        line = re.sub(r'(\S+)', r'\1/ntg', line)
        unigramV.append(line)
    input_vocab.append(line)

    if writeInDump == 'false' :
        outputF.write(line)

print "LENGTH of TRIGRAM : %d" % len(trigramV)
# print json.dumps(trigramV)
print "======================================"

print "LENGTH of BIGRAM : %d" % len(bigramV)
# print json.dumps(bigramV)
print "======================================"

print "LENGTH of UNIIGRAM : %d" % len(unigramV)
print json.dumps(unigramV)
print "======================================"

if writeInDump == 'true' :
    outputF.write(json.dumps(input_vocab))