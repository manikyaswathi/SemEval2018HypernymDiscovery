import os
import re
import json
import nltk
# from inputTerms import input_terms
# from getTags import unigramV, bigramV, trigramV
from nltk import word_tokenize

# trigramV = ["google earth" ,"gps devices"](one)
# bigramV = ["google/\S+ earth/\S+" ,"gps/\S+ devices/\S+"]
# trigramV = ["a/\S+ google/\S+ earth/\S+" ,"of/\S+ gps/\S+ devices/\S+"]
# (( [A-Z]+)? NN[A-Z]* ([A-Z]+ )?)|(( [A-Z]+)? ([A-Z]+)? NN[A-Z]* )
# bigramV = ["\S+/[A-Z]+ \S+/NN[A-Z]*"]
# trigramV = ["\S+/[A-Z]+ \S+/[A-Z]+ \S+/NN[A-Z]*"]

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
        # line = line.lower()
        if mD:
            # line = re.sub(r'(\S+) (\S+) (\S+)', r'\1/ntg \2/ntg \3/ntg', line)
            trigramVL.append(line)
        elif mS:
            # line = re.sub(r'(\S+) (\S+)', r'\1/ntg \2/ntg', line)
            bigramVL.append(line)
        else:
            # line = re.sub(r'(\S+)', r'\1/ntg', line)
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
    # print "----%s----" % val
    biPattern = biPattern + '('+val+')'+'|'
biPattern = biPattern + 'swathi'
biPattern = re.sub(r'\|swathi', r')', biPattern)
biPattern = re.sub(r'/nn ', r'/nn[a-z]* ', biPattern)
biPattern = re.sub(r'/nn$', r'/nn[a-z]*', biPattern)
print "bi-gram pattern : %s" % biPattern

for val in trigramV:
    # print "----%s----" % val
    triPattern = triPattern + '('+val+')'+'|'
triPattern = triPattern + 'swathi'
triPattern = re.sub(r'\|swathi', r')', triPattern)
triPattern = re.sub(r'/nn ', r'/nn[a-z]* ', triPattern)
triPattern = re.sub(r'/nn$', r'/nn[a-z]*', triPattern)
print "tri-gram pattern : %s" % triPattern

# print "--------------"
# print biPattern
# print "--------------"
# print triPattern
# print "--------------"

biPat = re.compile(r'%s' % biPattern)
triPat = re.compile(r'%s' % triPattern)

inputF = open("/home/manikya/Documents/NLP/Data/Sample.possf2",'r')
print "---------------"
for line in inputF:
    # print "here"
    Flist = []
    line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
    # unLine = re.sub(r'(\S+)/(\S+)', r'\1', line)(one)
    line = line.lower()
    unLine = line
    # unLine = unLine.lower()
    print line
    print "-----------------1----------------------"
    # line = re.sub(triPat, r'\1 D\1D', line)
    trigrammatch = re.findall(triPat, line, flags=0)
    list1= list(nltk.chain(*trigrammatch))
    print json.dumps(list1)
    print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    # trimatchL = []
    # for listItem in trigrammatch:
    #     listItem = filter(None, listItem)
    #
    #     trimatchL.append(listItem)
    # trimatchL = set(trigrammatch)

    # trigrammatch = filter("", trigrammatch)
    # print json.dumps(trimatchL)
    bigrammatch = re.findall(biPat, line, flags=0)
    list2 = list(nltk.chain(*bigrammatch))
    # list1.append(list2)
    # list = list(set(list))
    # print type(list)
    # elist = []
    # for item in list1:
    #     print "======================="
    #     print list(set(item))
    #     # print elist
        # Flist.append(list(set(item)))
    # Flist = list(set(Flist))
    # print json.dumps(Flist)

    # bigrammatch = re.findall(biPat, line, flags=0)
    # list.append(bigrammatch)
    lists = list1 + list2
    listF = list(set(lists))
    listFF = []
    for l in listF:
        l = re.sub(r'(\S+)/[a-z]+( ?)', r'\1\2', l)
        l = re.sub(r' ', r'_', l)
        l = l+"/nntb"
        listFF.append(l)
    print json.dumps(listFF)
    print "pppppppppppppppppppppppppppppppppppppppppppppppppppp"
    linen = " ".join(listFF)
    line = line + " " +linen
    print line
    samline = re.sub(r'((\S+/[^n][a-z]*)( )+)', r'', line)

    print "=================================================="
    print samline
    samline = re.sub(r'/[a-z]+', r'', samline)
    print "9090909090909090909090909090909090909090909099090909"
    print samline
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

