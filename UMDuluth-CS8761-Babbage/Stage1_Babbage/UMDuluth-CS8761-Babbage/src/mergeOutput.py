"""
Created on Thu Oct 12 18:20:52 2017

Author: Manilkya Swathi Vallabhajosyula
Team Babbage : CS 8761 Project
SemEval-2018 Task 9: Hypernym Discovery

Purpose : Merge the two output files (Co-occurnace output and Hearst output) into one to get a joint score

How to execute: 
python mergeOutput.py output_data_cooccur.txt output_data_hearst.txt output_data.txt

Where:
output_data_cooccur.txt           :   The output file created after creating the results from the normalised text i.e. by co-occurance. Stored at 'Output/' folder.
output_data_hearst.txt            :   The output file created after creating the results from the Hearst patterns. Stored at 'Output/' folder.
output_data.txt                   :   the output file created after merging the prevoius two files (line 1 output from one file is merged with line 1 output of the other file and so on.)

e.g. : 
python getTags ../Output/1A.english.output.trial.norm.txt ../Output/1A.english.output.trial.hearst.txt ../Output/1A.english.output.trial.merge.txt

e.g. Output
**********1A.english.output.trial.norm.txt****************[One line]
hurricane	island	damage	tate	wave	wind	relief	model	north	weather	insurance	coverage	disaster	flood	fund	
**********1A.english.output.trial.hearst.txt***************[One line]
various_community_organizations	
*********1A.english.output.trial.merge.txt*****************[One line]
hurricane	island	damage	tate	wave	wind	relief	model	north	weather	insurance	coverage	disaster	flood	fund	 various_community_organizations	

"""
# list of imports
import re
import nltk
import json
import sys
import time
from nltk import word_tokenize


print "[%s] Merging the Output Files\n" % time.ctime()
start_time = time.time()

argcount = len(sys.argv)
# At least 3 input parameters should be provided else the program does not work
if argcount < 4:
    print "Insufficient params for processing vocabulary\n"
    sys.exit()

# Input file 1 : Normalised cooccurance output
inputFilePath1 = sys.argv[1]
# Input file 2 : Hearst Pattern output
inputFilePath2 = sys.argv[2]
# Output file  : Merged output
outputFilePath = sys.argv[3]

inputF1 = open(inputFilePath1,"r") # read mode
inputF2 = open(inputFilePath2,"r") # read mode
outputF = open(outputFilePath,"w") # write mode

# lists to read the lines from both the files to stre as an array of strings
normOutput = []
hearstOutput = []

# Reading file 1 - Normalised Co-occurance output
for line in inputF1:
    normOutput.append(line)
inputF1.close()

# print "norm : %d \n" % len(normOutput)

# Reading file 2 - Hearts output
for line in inputF2:
    hearstOutput.append(line)
inputF2.close()

# Meringing the two files by appending the the respective lines: priority is given to co-occurance words as Hearts Pattrens are to be refined to unigram, bigram and triGram patterns
maxlength = len(normOutput)

for count in range(0, maxlength):
    line1 = re.sub(r'\n', r'', normOutput[count])
    line2 = re.sub(r'\n', r'', hearstOutput[count])
    string = line1 + " " + line2 + "\n"
    outputF.write(string)
outputF.close()

print "[%s] Completed merging the Output Files\n" % time.ctime()
