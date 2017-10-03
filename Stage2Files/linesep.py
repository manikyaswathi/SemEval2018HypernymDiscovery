import os
import re
import json
import nltk
import time
from nltk import word_tokenize

start_time = time.time()
unigramVL = []
bigramVL = []
trigramVL = []

unigramV = []
bigramV = []
trigramV = []


def prepPattern():
    singleUn = re.compile(r'(\S+) (\S+)')
    doubleUn = re.compile(r'(\S+) (\S+) (\S+)')
    openf = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/vocabulary/1A.english.vocabulary_1.txt",'r')
    for line in openf:
        mS = re.match(singleUn, line)
        mD = re.match(doubleUn, line)
        line = re.sub(r'\n', r'',line)
        if mD:
            trigramVL.append(line)
        elif mS:
            bigramVL.append(line)
        else:
            unigramVL.append(line)

prepPattern()
trigramVL.append('(\S+/nn[a-z]* \S+/nn[a-z]* \S+/nn[a-z]*)')
bigramVL.append('(\S+/nn[a-z]* \S+/nn[a-z]*)')
trigramV = set(trigramVL)
bigramV = set(bigramVL)
unigramV = set(unigramVL)
biPattern = '('
triPattern = '('

for val in bigramV:
    biPattern = biPattern + '('+val+')'+'|'

biPattern = biPattern + 'swathi'
biPattern = re.sub(r'\|swathi', r')', biPattern)
biPattern = re.sub(r'/nn ', r'/nn[a-z]* ', biPattern)
biPattern = re.sub(r'/nn$', r'/nn[a-z]*', biPattern)
# print "bi-gram pattern : %s" % biPattern

for val in trigramV:
    triPattern = triPattern + '('+val+')'+'|'

triPattern = triPattern + 'swathi'
triPattern = re.sub(r'\|swathi', r')', triPattern)
triPattern = re.sub(r'/nn ', r'/nn[a-z]* ', triPattern)
triPattern = re.sub(r'/nn$', r'/nn[a-z]*', triPattern)
# print "tri-gram pattern : %s" % triPattern

biPat = re.compile(r'%s' % biPattern)
triPat = re.compile(r'%s' % triPattern)


inputF = open("/home/manikya/Documents/NLP/Data/delorme.com_shu.pages_0.poss",'r')
# inputF = open("/home/manikya/Documents/NLP/Data/Sample.possf2",'r')
outputF = open("/home/manikya/Documents/NLP/DataV/delorme.com_shu.pages_0.txt",'w')
# outputF = open("/home/manikya/Documents/NLP/DataV/Sample.txt",'w')
# print "---------------"
for line in inputF:
    Flist = []
    line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
    line = line.lower()
    unLine = line
    # print line
    # print "-----------------1----------------------"
    trigrammatch = re.findall(triPat, line, flags=0)
    list1= list(nltk.chain(*trigrammatch))
    # print json.dumps(list1)
    # print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    bigrammatch = re.findall(biPat, line, flags=0)
    list2 = list(nltk.chain(*bigrammatch))
    lists = list1 + list2
    listF = list(set(lists))
    listFF = []
    for l in listF:
        l = re.sub(r'(\S+)/[a-z]+( ?)', r'\1\2', l)
        l = re.sub(r' ', r'_', l)
        l = l+"/nntb"
        listFF.append(l)
    # print json.dumps(listFF)
    # print "pppppppppppppppppppppppppppppppppppppppppppppppppppp"
    linen = " ".join(listFF)
    line = line + " " +linen
    # print line
    samline = re.sub(r'((\S+/[^n][a-z]*)( )+)', r'', line)

    # print "=================================================="
    # print samline
    samline = re.sub(r'/[a-z]+', r'', samline)
    samline = re.sub(r'(\S+)/(\1)', r'', samline)
    samline = re.sub(r'\n', r'', samline)
    # print "9090909090909090909090909090909090909090909099090909"
    # print samline
    samline = samline + '\n'
    outputF.write(samline)

    '''
    print "-----------------2---------------------"
    line = re.sub(r'D((\S+)/(\S+))( )+((\S+)/(\S+))( )+((\S+)/(\S+))D', r'\2_\6_\10/ntg', line)
    # print line
    print "-----------------3 TRI ABOVE---------------------"

    line = re.sub(biPat, r'\1 D\1D', line)
    print line
    print "-----------------4---------------------"
    line = re.sub(r'D((\S+)/(\S+))( )+((\S+)/(\S+))D', r'\2_\6/nbg', line)
    print line
    
    '''
    # samline = line
    '''
    print "-----------------5 BI ABOVE---------------------"

    samline = re.sub(r'((\S+/[^n][a-z]*)( )+)', r'', line)

    print "=================================================="
    print samline
    print "=================================================="
    '''
    # r'((\S+/\S+)( )+)*((\S+)/nn[a-z]*)?'

    # tagged_token = [nltk.tag.str2tuple(t) for t in line.split()]
    # tagged_token = nltk.tag.str2tuple(line)
    # print json.dumps(tagged_token)

print "The EXECUTION TIME is : %s" % (time.time() - start_time)