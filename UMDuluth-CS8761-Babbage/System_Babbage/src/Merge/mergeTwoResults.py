# -*- coding: utf-8 -*-
"""
Created on Sat Dec 02 11:50:56 2017

@author: Arshia
@modified By : swathi
"""

import re
from itertools import izip
import sys

'''                                                                                                                                           
input1 = Higher Rank File                                                                                          
input2 = Lower rank file                               
out = merged file                                                                                       
'''
input1 = open(sys.argv[1], "r")
input2 = open(sys.argv[2], "r")
out = open(sys.argv[3], "w")

# common elements + n from file 1 + n from file 2 + n from file 1 + n from file 2
# Pick top 15
# n = default 5
maxEachC = 5
maxEachS = 5
common_element = []
for CBOW, SG in izip(input1,input2):
    CBOW = re.sub(r'\n$', r'', CBOW)
    CBOW = re.sub(r'\t$', r'', CBOW)
    CBOW_line = CBOW.split('\t')
    SG = re.sub(r'\n$', r'', SG)
    SG = re.sub(r'\t$', r'', SG)
    SG_line = SG.split('\t')
    # extract file common elelmnets (higher rank)
    common_element = [w for w in CBOW_line if w in SG_line ]
    count = 0
    # n from file 1
    for new_word in CBOW_line :
        if count==maxEachC :
            break
        if count<maxEachC :
            if (new_word not in common_element) :
                common_element.append(new_word)
                count+=1
    count = 0
    # n from file 2 
    for new_word in SG_line :
        if count==maxEachS :
            break
        if count<maxEachS :
            if (new_word not in common_element) :
                common_element.append(new_word)
                count+=1
    count = 0
    # n from file 1
    for new_word in CBOW_line :
        if count==maxEachC :
            break
        if count<maxEachC :
            if (new_word not in common_element) :
                common_element.append(new_word)
                count+=1
    count = 0
    # n from file 2
    for new_word in SG_line :
        if count==maxEachS :
            break
        if count<maxEachS :
            if (new_word not in common_element) :
                common_element.append(new_word)
                count+=1
    output = ""
    for word in common_element :
        output = output + str(word) + '\t'
    output.strip('\n')
    output = re.sub(r'\t+', r'\t', output)
    output = re.sub(r'^\t+|\t+$', r'', output)
    output = re.sub(r'^((\S+\s+){0,15})(\S+\s+)*', r'\1', output) # Pick top 15
    output = output+'\n' 
    out.write(output)
input1.close()
input2.close()
