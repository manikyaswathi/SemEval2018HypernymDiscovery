import os
import re
import json
import nltk
# from inputTerms import input_terms
# from inputVocab import unigramV, bigramV, trigramV
from nltk import word_tokenize

# trigramV = ["google earth" ,"gps devices"](one)
# bigramV = ["google/\S+ earth/\S+" ,"gps/\S+ devices/\S+"]
# trigramV = ["a/\S+ google/\S+ earth/\S+" ,"of/\S+ gps/\S+ devices/\S+"]
# (( [A-Z]+)? NN[A-Z]* ([A-Z]+ )?)|(( [A-Z]+)? ([A-Z]+)? NN[A-Z]* )
bigramV = ["\S+/NN[A-Z]* \S+/[A-Z]+" ,"\S+/[A-Z]+ \S/NN[A-Z]*"]
trigramV = ["\S+/NN[A-Z]* \S+/[A-Z]+ \S+/[A-Z]+" ,"\S+/[A-Z]+ \S+/[A-Z]+ \S/NN[A-Z]*", "\S+/[A-Z]+ \S/NN[A-Z]* \S+/[A-Z]+"]
biPattern = '('
triPattern = '('

for val in bigramV:
    print "----%s----" % val
    biPattern = biPattern + '('+val+')'+'|'
biPattern = biPattern + 'swathi'
biPattern = re.sub(r'\|swathi', r')', biPattern)
print "bi-gram pattern : %s" % biPattern

for val in trigramV:
    print "----%s----" % val
    triPattern = triPattern + '('+val+')'+'|'
triPattern = triPattern + 'swathi'
triPattern = re.sub(r'\|swathi', r')', triPattern)
print "tri-gram pattern : %s" % triPattern

print "--------------"
print biPattern
print "--------------"
print triPattern
print "--------------"

biPat = re.compile(r'%s' % biPattern)
triPat = re.compile(r'%s' % triPattern)

inputF = open("/home/manikya/Documents/NLP/Data/Sample.possf2",'r')
print "---------------"
for line in inputF:
    print "here"
    line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
    # unLine = re.sub(r'(\S+)/(\S+)', r'\1', line)(one)
    line = line.lower()
    unLine = line
    # unLine = unLine.lower()
    print line
    print "-----------------1----------------------"
    line = re.sub(triPat, r'\1 @\1@', line)
    print line
    print "-----------------2---------------------"
    line = re.sub(r'@((\S+)/(\S+))( )+((\S+)/(\S+))( )+((\S+)/(\S+))@', r'\2_\6_\10/ntg', line)
    print line
    print "-----------------3 TRI ABOVE---------------------"

    line = re.sub(biPat, r'\1 @\1@', line)
    print line
    print "-----------------4---------------------"
    line = re.sub(r'@((\S+)/(\S+))( )+((\S+)/(\S+))@', r'\2_\6/nbg', line)
    print line
    # samline = line
    print "-----------------5 BI ABOVE---------------------"

    samline = re.sub(r'((\S+/[^n][a-z]*)( )+)', r'', line)

    print "=================================================="
    print samline
    print "=================================================="

    # r'((\S+/\S+)( )+)*((\S+)/nn[a-z]*)?'

    tagged_token = [nltk.tag.str2tuple(t) for t in line.split()]
    # tagged_token = nltk.tag.str2tuple(line)
    # print json.dumps(tagged_token)