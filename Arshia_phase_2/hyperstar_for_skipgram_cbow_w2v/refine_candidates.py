# -*- coding: utf-8 -*-
"""
@author: Arshia Zernab Hassan
@team : Babbage

@File_name : refine_candidates.py
Module to refine candidates produced by evaluate.py module of hyperstar system. 
It reads input file line by line and discards candidates which are not present in the provided vocabulary and produces refined candidate lists.
The input file contain tab separated candidate hypernyms in each line. The output file is of the same format.

Command line arguments :
argument 1 : input file path
argument 2 : output file path

Example run :
python refine_candidates.py output_hyperstar output_refine
"""

from collections import defaultdict
import os
import re
import sys

"""
#Function name : load_vocab_to_list
#Author : Arshia Zernab Hassan
#Function description : 
-reads from file the list of vocabulary to a list
#Input Parameters : 
filename (name of the file that contains vocabulary of hypernyms)
#Output : 
A list of vocabulary 
#pre-condition : 
    1.filename is valid
    2.file contains vocabulary word at each line
""" 
def load_vocab_to_list(file_name) :    
    try:
        vocab_list = list()
        file_ptr = open(file_name,'r') #open file
        for line in file_ptr :
            vocab = line.strip()
            vocab_list.append(vocab)
        file_ptr.close() #close file         
        return vocab_list
    except IOError:
        print "Could not open file!"

vocab_file = "1A.english.vocabulary.txt"        
vocab_list=load_vocab_to_list(vocab_file)

in_file_name = sys.argv[1]
out_file_name = sys.argv[2]
in_file_ptr = open(in_file_name, "r")
out_file_ptr = open(out_file_name, "w")

#reads input file line by line, only select words available in vocabulary, create tab separated string of hypernyms and write to output file
for line in in_file_ptr :
    line = re.sub(r'\n$', r'', line)
    line = re.sub(r'\t$', r'', line)
    line_list = line.split('\t')
    new_list = []
    for word in line_list :
        if word in vocab_list :
            new_list.append(word)
    output = ''
    for word in new_list :
        output = output + str(word) + '\t'
    output.strip('\n')
    output = output+'\n'
    out_file_ptr.write(output)

in_file_ptr.close()
out_file_ptr.close()
