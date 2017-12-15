import os
import re
import time
import sys
import nltk

start_time = time.time()
# NORMALIZE HEARTS

# @AUTHOR: MANIKYA SWATHI VALLABHAJOSYULA
# PURPOSE : To extarct new Hearst Patterns of stage 2  NP1 is (a|an|the) NP0 
# Run : python Hearst_Pattern_Stage2_IsA.p input_folder/ output_folder/
# input : an iphone is a phone
# Stage 2 IS-A pattern : iphone : phone

# THis is used for Stage2 - Model1

filepath = sys.argv[1]                # Input path for tagged UMBC corpus
ofilepath = sys.argv[2]               # Output path to store NP1 is (a|an|the) NP0 patterns obtainted from input corpus

# the pattern which checks for presence of is (a|an|the)
isa_tags = re.compile(r' is/\S+ (?:a|an|the)/\S+ ')

# The folder is read file by file
for file in os.listdir(filepath):
    if ".possf2" in file:
        # for all the possf2 files the pattern is extracted
        # opening one input file at a time
        inputFN = filepath + file
        inputF = open(inputFN, 'r')
        # Opening one output file per input file
        oFile = re.sub(r'.possf2', r'_ISaat.txt', file)
        oFile = ofilepath + oFile
        outputHF = open(oFile, 'w')
        # For each line of the file
        for line in inputF:
            line = " "+line
            line = line.lower()
            # Converts _ to / separation of word, POS tag
            line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
            # The is-a pattern ins lokked up in the file and if there is a match, then the if call proceeds
            matchisa = re.search(isa_tags, line)
            if matchisa:
                # NP patterns for NP1 and NP0 for NP1 is (a|an|the) NP0
                # np is the pattern match for NP1 
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+'
                # np2 and lsep are patterns for NP0
                np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:,/, +)?(?:(?:(?:and)|(?:or))/cc))?)'
                lsep = '(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+'
                # pattern = re.compile(r'(?:(?:%s +%s)|(?:%s +%s)) is/\S+ +(?:a|an|the)/\S+ +(?:%s )?%s' % (np, npP, npP, np, np2, lsep))
                pattern = re.compile(r'%s is/\S+ +(?:a|an|the)/\S+ +(?:%s )?%s' % (np, np2, lsep))
                # fetching all the patterns matched from a given line
                npTuple = re.findall(pattern, line, flags=0)
                for item in npTuple:
                    # For each NP1 is (a|an|the) NP0, process the NP0, NP1 to fpr the result in the fomat NP1 : NP0
                    # example : the tupe match is "cat/NN is/VBZ a/DT feline", the below substituttions converts this to "cat : feline" and
                    # stores in into the oupt file (all the patterns in output file are of "hyponym : hypernym" format
                    item = re.sub(r'(\S+)/(\S+)', r'\1', item)
                    formItem = re.sub(r' +', r'_', item)
                    formItem = re.sub(r'(_is_(a|an|the)_)', r' : ', formItem)
                    formItem = re.sub(r'(_,) : ', r' : ', formItem)
                    formItem = re.sub(r'(_,_)(and|or)_', r' , ', formItem)
                    formItem = re.sub(r'_,_', r' , ', formItem)
                    formItem = re.sub(r'_(and|or)_', r' , ', formItem)
                    formItem = re.sub(r'_$', r'', formItem)
                    formItem = re.sub(r'(\\/[a-zA-Z0-9]+_)', r'_', formItem)
                    # writing result to file
                    outputHF.write('%s \n' % formItem)
        # Closing the output file
        outputHF.close()
#print "The EXECUTION TIME is : %s" % (time.time() - start_time)
