"""
Created on Thu Oct 03 01:00:00 2017

Author: Manilkya Swathi Vallabhajosyula
Team Babbage : CS 8761 Project
SemEval-2018 Task 9: Hypernym Discovery

Purpose : Fetch the POS patterns of input vocabulary file after tagging it with nltk tagger. 
The patterns which occur more than 100 times are considered for bi-gram and tri-gram patterns

How to execute: 
python getTags.py input_vocabulary_file.txt intermediate_vocab.txt final_top_POS_tag_patterns.txt

Where:
input_vocabulary_file.txt           :   The vocabulary file '1A.english.vocabulary.txt' given with semval data @ 'SemEval18-Task9/vocabulary/' folder
intermediate_vocab.txt              :   The intermediate vocabulary file '1A.english.vocabulary_0.txt' created after tagging '1A.english.vocabulary.txt' file given with semval data @ 'SemEval18-Task9/vocabulary/' folder. Tagger used from NLTK Toolkit
final_top_POS_tag_patterns.txt      :   The final vocabulary file '1A.english.vocabulary_1.txt' created after analysing the '1A.english.vocabulary_0.txt' file for the most used patterns (over 100) for bi-gram and tri-gram data.

e.g. : 
python getTags.py ../SemEval18-Task9/vocabulary/1A.english.vocabulary.txt ../SemEval18-Task9/vocabulary/1A.english.vocabulary_0.txt ../SemEval18-Task9/vocabulary/1A.english.vocabulary_1.txt

e.g. Output
**********Input File****************
a battery
a capella singing
ballet
ballet company
**********Interm File***************
 a/DT battery/NN 
 a/DT capella/NN singing/NN
 ballet/NN 
 ballet/NN company/NN
**********OutPut File***Patterns occuring more than 100 times in 218759 tagged lines********
\S+/jj \S+/nn \S+/nn
\S+/rb \S+/nn
..........
..........
..........
\S+/nn \S+/cc \S+/nn
\S+/nn \S+/in \S+/nns

"""

# Import dependencies
import re
import nltk
import json
import sys
import time
from nltk import word_tokenize

argcount = len(sys.argv)
# If command line arguments are not at least 3, this process will not execute
if argcount < 4:
    print "Insufficient params for processing vocabulary\n"
    sys.exit()
# The input Vocal file
inputFilePath = sys.argv[1]
# The interm tagged vocab file
intermFilePath = sys.argv[2]
# The final vocal file with populat POS bi-gram tri-gram tags
outputFilePath = sys.argv[3]

# Opening input file in read mode
inputF = open(inputFilePath,"r")
# Opening the intermediate and the final file in write mode
outputF = open(intermFilePath,"w")
outputF1 = open(outputFilePath,"w")

# Holds all tag patterns 
taglist = []

# Reading through the vocab file
# Tagging each line
# Extract just the tag from the tagged line and insert it into the list
for line in inputF:
    tokens = nltk.word_tokenize(line)
    tagggedT = nltk.pos_tag(tokens)
    temp = " "
    temp2 = " "
    for eachToken in tagggedT:
        temp2 = temp2+eachToken[0]+"/"+eachToken[1]+" "
        temp = temp+eachToken[1]+" "
    taglist.append(temp)
    temp2 = temp2 + "\n"
    outputF.write(temp2)
tagset = set(taglist)
# print tagset

count  = 0
# Fetting the tag patterns which appear more than 100 times
for val in tagset:
    mt = re.match(r'^(( [A-Z]+)? ([A-Z]+ )?NN[A-Z]* )$', val)
    if mt:
        temp = val + "/" + str(taglist.count(val)) +"\n"
        if (taglist.count(val) > long(100)) :
            val = val.lower()
            val = re.sub(r' ([a-z]+)', r' \S+/\1', val)
            val = re.sub(r'(^ )|( $)',r'',val)
            outputF1.write(val)
            outputF1.write('\n')
        count += 1


