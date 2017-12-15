import re
import nltk
import os
import operator
import time
import sys

# AUTHOR : MANIKYA SWATHI VALLABHAJOSYULA
# PURPOSE: TO FIND TWO DIFFERNT TYPE OF RESULTS
'''
1. For bi/tri-gram Concepts: apply part-of analogy to fetch one candidate hypernym
2. Apply IS-A pattern to all target words
'''
# run as :
# python filename trial/training-data
# python Stage2Model1IsA.py 1A.english.(training|trial).data.txt
#------------------------------------------------------------------------------------------------------
# Function(wordL)
# Input - target word (hyponym)
# ouput - list of hyperns from IS-A pattern
# IMPORTANT FILE = UMBCCEIS.txt - the IS-A Patterns from UMBC corpus = 2,633,421 pairs
# Example:
'''
Input Word: tropical storm (concept)
UMBCCEIS.txt : matches
          Hearts patterns obtained from UMBC Corpus:
          tropical storm emily : fifth named storm
          tropical storm allison : focus
          tropical storm mitch : prime example
          tropical storm alberto : reminder
          a tropical storm : formation
          tropical storm florence : sixth named storm
Oputput = Retrieved Hypernym list: {example, storm, reminder, focus, hurricane}
'''
def lookUpHearstIsPatter(wordL):
    stringRet = ""
    # inputFHI = "/home/manikya/Documents/NLP/Stage2_T2/UMBCCEIS/UMBCCEIS.txt"
    inputFN = "UMBCCEIS.txt"
    inpF = open(inputFN, 'r')
    for cline in inpF:
        cline = cline.lower()                          
        hypoT = re.sub(r'(\S+) +: +(\S+)', r'\1', cline)
        lookUpWord = "(?:^|_| )"+wordL+"(?: |_(?:[\w-]+)|$)"
        lookUpWordP = re.compile(r'%s' % lookUpWord)
        foundW = re.search(lookUpWordP, hypoT)
        if foundW:
            lineHyper = re.sub(r'(\S+) +: +(\S+)', r'\2', cline)
            lineHyper = re.sub(r'\n', r'', lineHyper)
            stringRet = stringRet + lineHyper + ", "
    return stringRet

# The Candiadte Vocabulary file - 218,755 candidate hypernyms
inputFV = open("1A.english.vocabulary.txt","r")

# creating the list of vocabulary
input_vocab = []

for line in inputFV:
    inputV = re.sub(r'^\s+', r'', line)
    inputV = re.sub(r'\s+$', r'', inputV)
    inputV = re.sub(r'\s+', r'_', inputV)
    input_vocab.append(inputV)

input_set = set(input_vocab)

# Function (from output of def lookUpHearstIsPatter) - given as listOfWords:
# Inputwords - listOfWords
# Output = refined hypernym list
# Process
'''
1. item in list - fond in vocab keep
2. else repetedly apply back-off (tri-grams to bi-grmas to unigrams till the word is found in vocab list
3. Elase discard if not found at all
'''
def wordsInVocab(listOfWords):
    returnStr = " "
    possibleW = listOfWords.strip().split(",")
    for item in possibleW:
        item = re.sub(r'^ +', r'', item)
        item = re.sub(r' +$', r'', item)
        if item in input_set:
            # 1. item found
            returnStr = returnStr + item + " , "
        else:
            # match undersre to detemine not-a unigram
            matchU = re.search(r'_', item)
            if matchU:
                # match for bi-gram or tr-gram pattern in item
                matchT = re.search(r'[\w-]+_\S+_\S+_\S+$',item)
                matchB = re.search(r'^[\w-]+_\S+$', item)
                if matchT:
                    # first look for tri-gram
                    triItem = re.sub(r'[\w-]+_(\S+)_(\S+)_(\S+)$', r'\1_\2_\3', item)
                    if triItem in input_set:
                        # tri-gram found
                        returnStr = returnStr + triItem + " , "
                    else:
                        # if trigram not found
                        # extract a bi-gram
                        biItem = re.sub(r'\S+_(\S+)_(\S+)$', r'\1_\2', triItem)
                        if biItem in input_set:
                            # bigram found
                            returnStr = returnStr + biItem + " , "
                        else:
                            # if Bigram not found
                            # extract unigram
                            uniItem = re.sub(r'\S+_(\S+)$', r'\1', biItem)
                            if uniItem in input_set:
                                # found unigram
                                returnStr = returnStr + uniItem + " , "
                elif matchB:
                    # if no match for trigrams of back-of bi/uni-grams of term
                    # and the bi-gram is also not found
                    # look for unigram
                    uniItem = re.sub(r'\S+_(\S+)$', r'\1', item)
                    if uniItem in input_set:
                        # unigram found
                        returnStr = returnStr + uniItem + " , "
    # refine the result by creating the sets - removing the diblicates
    possibleW = returnStr.strip().split(" , ")
    possibleW = set(possibleW)
    finalStr = ""
    # list of hypernyms
    PList = []
    # list of counts for hypernyms
    Nlist = []
    # for each word in set, find the count in the original list
    # example : cat puppy cat fur cat fur fur fur
    # cat:3 puppy:1 fur:4
    for res in possibleW:
        res = re.sub(r'^ +', r'', res)
        res = re.sub(r' +$', r'', res)
        searchStr = "(?:_| )"+res+"(?:_| )"
        searchPattern = re.compile(r'%s' % searchStr)
        listI = re.findall(searchPattern, returnStr)
        count = len(listI)
        PList.append(res)
        Nlist.append(count)
    # sorts the hypoernym list based on frequency
    # e.g. puppy:1, cat:3, fur:4
    RetList = [k for k, v in sorted(zip(PList, Nlist), key=operator.itemgetter(1))]
    # reverse the list fur:4, cat:3, puppy:1,
    RetList.reverse()
    # cratea a tab separated string of hypernym list and take only TOP 10
    for hypernym in RetList:
        finalStr = finalStr + hypernym + "\t"
    finalStr = re.sub(r' +$', r'', finalStr)
    finalStr = re.sub(r'^((\S+\s+){0,10})(\S+\s+)*', r'\1', finalStr)
    finalStr = re.sub(r' +$', r'', finalStr)
    return finalStr

# Input file - TRAIN|TRIAL
inputFileName = sys.argv[1]
# USE THE INPUT FILE NAME for OUTPUT
outputFileName = inputFileName+".op.txt"
# open the input and oputput files for reading and writing  respectively
inputF = open(inputFileName,"r")
outputF = open(outputFileName,"w")

# ALGORITHM:
'''
1. Read input word from input file
2. get the target word
3. get either concept or entuty
4. tag POS for target word (used for Part-Of module)
5. If the word is Concept
   i.  If the word is tri-gram 
       a. with IN -POS tag  : get the first word of tri-gram as hypernym
       b. without IN -POS tag : get the third word from trigram as hypernym
   ii. If the word is bi-gram : get the send word of bi-gram as hypernym
   iii. for all concepts look for IS-A pattern's hyponym section and get all hypernyms
6. If the word is Entuty look for IS-A pattern's hyponym section and get all hypernyms 
7. If not found at all return an empty line
'''
for line in inputF:
    splitline = line.strip().split("\t")
    TarWord = splitline[0]                           # get target word from input
    TarType = splitline[1]                           # get target word's type from input
    matchTypeC = re.compile(r'\b[Cc]oncept\b')
    matchTypeE = re.compile(r'\b[Ee]ntity\b')
    tokens = nltk.word_tokenize(TarWord)
    tagggedT = nltk.pos_tag(tokens)
    temp = " "
    temp2 = " "
    hyp = ""
    # TAG ALL the words i=of input word
    for eachToken in tagggedT:
        temp2 = temp2+eachToken[0]+"/"+eachToken[1]+" "
    matchedC = re.search(matchTypeC, TarType)
    matchedE = re.search(matchTypeE, TarType)
    if matchedC:
        # matching for concpet
        matchTG = re.search(r'^ *\S+/\S+ +\S+/\S+ +\S+/\S+ *$', temp2)
        matchBG = re.search(r'^ *\S+/\S+ +\S+/\S+ *$', temp2)
        matchUG = re.search(r'^ *\S+/\S+ *$', temp2)
        # 5. i.
        if matchBG:
            getBiNN = re.match(r'^ *\S+/\S+ +(\S+)/(\S+) *$', temp2)
            matchNNOnly = re.match(r'^(?:nn)|(?:vb)[a-z]*', getBiNN.group(2).lower())
            if matchNNOnly:
                hyp = hyp + getBiNN.group(1)
        if matchTG:
            # 5. ii.
            getTriNN = re.match(r'^ *(\S+)/(\S+) +(\S+)/(\S+) +(\S+)/(\S+) *$', temp2)
            matchSNOnly = re.match(r'^(?:nn)|(?:vb)[a-z]*', getTriNN.group(2).lower())
            matchINOnly = re.match(r'^in', getTriNN.group(4).lower())
            matchLNOnly = re.match(r'^(?:nn)|(?:vb)[a-z]*', getTriNN.group(6).lower())
            if matchINOnly:
                hyp = hyp + getTriNN.group(1)
            elif matchLNOnly:
                hyp = hyp + getTriNN.group(5)
        '''
        if matchUG:
            wordToFun = re.sub(r' +', r'_', TarWord)
            wordToFun = wordToFun.lower()
            listL = lookUpHearstIsPatter(wordToFun)
            resList = wordsInVocab(listL)
            resList = re.sub(r'(\S+)\t\1 ,', r'\1', resList)
            resList = re.sub(r' ,', r'', resList)
            hyp = hyp + resList
        '''
        # 5. iii.
	wordToFun = re.sub(r' +', r'_', TarWord)
        wordToFun = wordToFun.lower()
        listL = lookUpHearstIsPatter(wordToFun)
        resList = wordsInVocab(listL)
        resList = re.sub(r'(\S+)\t\1 ,', r'\1', resList)
        resList = re.sub(r' ,', r'', resList)
        hyp = hyp + "\t" +resList
        hyp = re.sub(r'^\s+|\s+$', r'', hyp)
	hyp = hyp + "\n"
        outputF.write(hyp)
    elif matchedE:
        # 6. match for entity
        wordToFun = re.sub(r' +', r'_', TarWord)
        wordToFun = wordToFun.lower()
        listL = lookUpHearstIsPatter(wordToFun)
        resList = wordsInVocab(listL)
        resList = re.sub(r'(\S+)\t\1 ,', r'\1', resList)
        resList = re.sub(r' ,', r'', resList)
        hyp = hyp + resList
        hyp = re.sub(r'^\s+|\s+$', r'', hyp)
        hyp = hyp + "\n"
        outputF.write(hyp)
    else:
        # If there is no match foe either modules, enter a blanlk line
        hyp = hyp + "\n"
        outputF.write(hyp)
