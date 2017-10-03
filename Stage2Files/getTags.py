# This program prints Hello, world! SPACE TRIMMING START END, SENTENCES in QAUT$
import re
import nltk
import json
import statistics
from nltk import word_tokenize
# from collections import defaultdict

print 'Starting the Processing\n'

inputF = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/vocabulary/1A.english.vocabulary.txt","r")
outputF = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/vocabulary/1A.english.vocabulary_0.txt","w")
outputF1 = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/vocabulary/1A.english.vocabulary_1.txt","w")
outputF2 = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/vocabulary/1A.english.vocabulary_2.txt","w")
outputF3 = open("/home/manikya/Documents/NLP/Data/SemEval18-Task9/vocabulary/1A.english.vocabulary_3.txt","w")

unigramV = []
bigramV = []
trigramV = []

writeInDump = 'false'

input_vocab = []

# PULL THIS OFF
# singleUn = re.compile(r'(\S+) (\S+)')
# doubleUn = re.compile(r'(\S+) (\S+) (\S+)')

taglist = []

for line in inputF:
    tokens = nltk.word_tokenize(line)
    tagggedT = nltk.pos_tag(tokens)
    temp = " "
    temp2 = " "
    for eachToken in tagggedT:
        temp2 = temp2+eachToken[0]+"/"+eachToken[1]+" "
        temp = temp+eachToken[1]+" "
        # print eachToken[1]
        # print "---------------"
    taglist.append(temp)
    temp2 = temp2 + "\n"
    outputF.write(temp2)
    # print "***********temp %s *************" % temp
tagset = set(taglist)
print tagset

countset =[]
countval =[]

count  = 0
for val in tagset:
    # mt = re.match(r'^(( [A-Z]+)? NN[A-Z]* ([A-Z]+ )?)|(( [A-Z]+)? ([A-Z]+)? NN[A-Z]* )$', val)
    mt = re.match(r'^(( [A-Z]+)? ([A-Z]+ )?NN[A-Z]* )$', val)
    if mt:
        # print "========%s======" % val
        # print taglist.count(val)
        # outputF1.write("--%s--%d\n" % (val,taglist.count(val)))
        temp = val + "/" + str(taglist.count(val)) +"\n"
        if (taglist.count(val) > long(100)) :
            val = val.lower()
            val = re.sub(r' ([a-z]+)', r' \S+/\1', val)
            val = re.sub(r'(^ )|( $)',r'',val)
            # outputF1.write(temp)
            outputF1.write(val)
            outputF1.write('\n')
            ''' PULL THIS OFF
            mS = re.match(singleUn, val)
            mD = re.match(doubleUn, val)
            if mD:
                # line = re.sub(r'(\S+) (\S+) (\S+)', r'\1/ntg \2/ntg \3/ntg', line)
                trigramV.append(val)
            elif mS:
                # line = re.sub(r'(\S+) (\S+)', r'\1/ntg \2/ntg', line)
                bigramV.append(val)
            else:
                # line = re.sub(r'(\S+)', r'\1/ntg', line)
                unigramV.append(val)
            PULL THIS OFF    '''
            # countset.append(val)
            # countval.append(taglist.count(val))
            # countset[count]=val
            # countval[count]=taglist.count(val)
        count += 1


'''
countt = 0
for value in countset:
    if countval[countt] > 100 :
        outputF3.write("--%s--%d\n" % (value, countval[countt]))
    countt += 1
print "count = %d" % count

# countval = sorted(countval)

# medVal = statistics.median(countval)
medVal = 50
newcount = 0
for x in range(0, count-1):
    if countval[x] > medVal:
        outputF2.write("%s====%d\n" % (countset[x],countval[x]))
        newcount += 1
        # print "&&&&&&&&&&&&&&&&&&&&&&&&&&&"

print "-------------MedVal--%d--------------" %medVal
print "-------------newcount--%d--------------" %newcount
# for line in inputF:
#     lineU = re.sub(r' ', r'_', line)
#     lineU = re.sub(r'\n$', r'', lineU)
#     lineU = lineU.lower()
#     lineU = lineU.lower()
#     line = lineU
#     mS = re.match(singleUn, lineU)
#     mD = re.match(doubleUn, lineU)
#     if mD:
#         line = re.sub(r'(\S+)_(\S+)_(\S+)', r'\1/ntg \2/ntg \3/ntg', line)
#         trigramV.append(line)
#     elif mS:
#         line = re.sub(r'(\S+)_(\S+)', r'\1/ntg \2/ntg', line)
#         bigramV.append(line)
#     else:
#         line = re.sub(r'(\S+)', r'\1/ntg', line)
#         unigramV.append(line)
#     input_vocab.append(line)
#
#     if writeInDump == 'false' :
#         outputF.write(line)
#
# print "LENGTH of TRIGRAM : %d" % len(trigramV)
# # print json.dumps(trigramV)
# print "======================================"
#
# print "LENGTH of BIGRAM : %d" % len(bigramV)
# # print json.dumps(bigramV)
# print "======================================"
#
# print "LENGTH of UNIIGRAM : %d" % len(unigramV)
# print json.dumps(unigramV)
# print "======================================"
#
# if writeInDump == 'true' :
#     outputF.write(json.dumps(input_vocab))
'''