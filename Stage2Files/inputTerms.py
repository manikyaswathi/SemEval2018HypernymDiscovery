# This program prints Hello, world! SPACE TRIMMING START END, SENTENCES in QAUT$
import re
import nltk
import json
from nltk import word_tokenize
# from collections import defaultdict

print 'Starting the Processing\n'

inputF = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/trial/data/1A.english.trial.data.txt","r")
outputF = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/trial/data/1A.english.trial.data_O.txt","w")

writeInDump = 'false'

input_terms = dict()

input_terms['concept'] = []
input_terms['entity'] = []

for line in inputF:
    line = re.sub(r'([\w]) ([\w])', r'\1_\2', line)
    line = line.lower()
    tokens = word_tokenize(line)
    input_terms[tokens[1]].append(tokens[0])
    if writeInDump == 'false' :
        outputF.write('{0}\t{1}\n'.format(tokens[1], tokens[0]))

if writeInDump == 'true' :
    outputF.write(json.dumps(input_terms))

