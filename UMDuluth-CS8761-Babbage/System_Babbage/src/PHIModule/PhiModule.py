import time
import re
import gensim, logging
from stemming.porter2 import stem
import numpy as np
import math
import sys

# Author: Manikya Swathi vallabhajosyula
# PURPOSE: remoiving word embeddings from the vector space model (with seed cat-anima)
# but Determine the hypernyms of a given hyponym based on PHI distance
# refernce : Learning Semantic Hierarchies via Word Embeddings https://www.aclweb.org/anthology/P/P14/P14-1113.xhtml
# INPUT: training or trial data
# OPUTPUT: top 15 possible hypernyms for training or trial data
# run as:
# COMMAND ARGUMNETS
# ARG 1 : WORD EMBEDIING MATRIX - UMBCNewNormNoStopHearst_CBOW_20_10 or UMBCNewNormNoStopHearst_SG_20_10
# ARG 2 : 1A.english.(training|trial).data.txt
# ARG 3 : PHI01 file name Phi01.txt
# ARG 4 : PHI02 file name Phi02.txt
'''
python PhiModule.py UMBCNewNormNoStopHearst_CBOW_20_10 1A.english.trial.data.txt phi01.txt phi02.txt
'''
# ALGORITHM: Algorithm.txt in the same formulae
# PHI01
'''
mayfly  chironomid      simulium        ephemeroptera   killifish       cyprinus        diptera piscivorous     mosquitofish    phalacrocorax 
  odonata herbivorous     insectivorous   chub    lepomis orthoptera
'''
# PHI02
'''
mayfly  chironomid      simulium        ephemeroptera   diptera killifish       cyprinus        phalacrocorax   mosquitofish    trematode     
  herbivorous     insectivorous   chub    sunfish piscivorous     salvinia
'''
# THE HYPERNYMS which exit in bothe the files are given a higher RANK
'''
mayfly  chironomid      simulium        ephemeroptera   diptera killifish       cyprinus        phalacrocorax   mosquitofish      herbivorous     insectivorous   chub    
'''



# logging the results of this module
logging.basicConfig(filename='Model2.LOG', filemode='w' ,format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
# The seed FILES for calculating PHI
inputFD = open("1A.english.training.data.txt","r")
inputFG = open("1A.english.training.gold.txt","r")

lineCount = 0
resCount = 0
countC = 0
countE = 0

ListIT = []
ListGD = []

# STEP 1

logging.info('Reading the seed files:')
logging.info('1.  reading the hyponyms')
for line in inputFD:
    lineCount = lineCount + 1
    line = line.lower()
    splitline = line.strip().split("\t")
    TarWord = splitline[0]
    TarType = splitline[1]
    TarWord = re.sub(r'^\s+|\s+$',r'', TarWord)
    TarWord = re.sub(r'\s+', r'_', TarWord)
    ListIT.append(TarWord)

logging.info('2.  reading the hypernyms')
for line in inputFG:
    resCount = resCount + 1
    line = line.lower()
    line = re.sub(r'^\s+|\s+$',r'', line)
    line = re.sub(r'\t',r';',line)
    line = re.sub(r'\s', r'_', line)
    ListGD.append(line)

pairITGD = []
countA = 0

logging.info('3. Creating the seed pairs (hyponym, hypernym) from read files ')
for i in range(0,lineCount-1):
    word = ListIT[i]
    res = ListGD[i]
    splitRes = res.strip().split(";")
    for entry in splitRes:
        countA =countA+1
        copyPair = word+"="+entry
        pairITGD.append(copyPair)

# FUNCTION (hyponym, hypernym)
# input : vector:hyponym, vector:hypernym
# output : the  right side of equation 1  from swathi_stage2_report
def computeNormPhiXminYSq(phi, x, y):
    phix = phi*x
    phyxminy= np.subtract(phix, y)
    nphyxminy = np.linalg.norm(phyxminy)
    finalval = math.pow(nphyxminy,2.0)
    return finalval

#=============================================================================================================
# READ the VOcabulari fily file a create a look up list
logging.info('Reading the Vocabulary file: the candiate hypernyms provided with the task')
inputFVoc = open("1A.english.vocabulary.txt","r")
input_vocab = []
for line in inputFVoc:
    inputV = re.sub(r'^\s+', r'', line)
    inputV = re.sub(r'\s+$', r'', inputV)
    inputV = re.sub(r'\s+', r'_', inputV)
    input_vocab.append(inputV)
input_set = set(input_vocab)

# FUNCTION: (A possible Hypernym)
# INPUT: hypernym
# OUTPUT: Refined hypernym (look up in vocab)
# Algorith
'''
1. item in list - fond in vocab keep
2. else repetedly apply back-off (tri-grams to bi-grmas to unigrams till the word is found in vocab list
   Along with back-off aplly steeming to sub words too
3. Else discard if not found at all  
'''
def GetLookUpWord(resString):
    resTokens = re.split(r'\t+', resString)
    finalTempStr = ""
    for vocab in resTokens:
        # if cound the word merge in result
        if vocab in input_set:
            finalTempStr = finalTempStr + vocab + "\t"
        else:
            # if not found, look for stem word
            stemVocab = stem(vocab)
            if stemVocab in input_set:
                # stem word found
                finalTempStr = finalTempStr + stemVocab + "\t"
            else:
                # even thestemmed output is not found
                # look for bi-gram and stem each word of the bi-gram merge it and looks for the new bigram
                tokenInp = vocab.strip("_")
                if len(tokenInp) > 1 and len(tokenInp) < 3:
                    t1 = stem(tokenInp[0])
                    t2 = stem(tokenInp[1])
                    putWord = t1 + "_" + t2
                    if putWord in input_set:
                        # stemmed bi-gram found
                        finalTempStr = finalTempStr + putWord + "\t"
                elif len(tokenInp) > 2 and len(tokenInp) < 4:
                    # if the word is a trigram
                    # Apply stemming to all sub-words, reform the stemmed tri-gram and look in vocab
                    t1 = stem(tokenInp[0])
                    t2 = stem(tokenInp[1])
                    t3 = stem(tokenInp[2])
                    putWord = t1 + "_" + t2 + "_" + t3
                    if putWord in input_set:
                        # found the stemmed tri-gram
                        finalTempStr = finalTempStr + putWord + "\t"
    #print "%s" % finalTempStr
    return finalTempStr

logging.info('Assigning the Test File/Sample file and output files: ')
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#===============================================================================================================+
# READING THE SAMPLE DATA INPUT FILE TRAIL OR TRAINING AND CREATING TWO DIFFERNT PUTPUT FILES - PHI01 and PHI02 + 
#===============================================================================================================+
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# the ARG 2 = Thr training or trial data 1A.engligh.(training|trial).data.txt
Sample_Data_File = sys.argv[2]
logging.info('1.  The sample data with target words (hyponyms): %s'% Sample_Data_File)
filepath = Sample_Data_File
# Phi: training                   Analogy : + = [word; y(=phix)] | - = []
# the ARG 3 = Stage2_Phi01_(train|trial).txt
outputFile = sys.argv[3]
logging.info('1.  The output file ONE (candidate hypernyms) : %s'% outputFile)
logging.info('     candidates fetched from : most_similar(positive=[input word vector, PHI VECTOR * input word vector], negative=[]) ')
inputF = open(filepath, 'r')
outpuO = open(outputFile, 'w')

# Opening input again with new output stream
filepath2 = Sample_Data_File
inputF2 = open(filepath2, 'r')
# Phi: training                   Analogy : + = [word] | - = [y(=phix)]
# the ARG 4 = Stage2_Phi02_(train|trial).txt
outputFile2 = sys.argv[4]
logging.info('2.  The output file TWO (candidate hypernyms) : %s'% outputFile2)
logging.info('     candidates fetched from : most_similar(positive=[input word vector] negative=[PHI VECTOR * input word vector]) ')
outpuO2 = open(outputFile2, 'w')

count = 100
#==========================================================================================
logging.info('ASSIGNING THE WORD2VEC MODEL')
# the ARG 1 =The word embedding matrix UMBCNewNormNoStopHearst_SG_20_10 or UMBCNewNormNoStopHearst_CBOW_20_1
model_file = sys.argv[1]
logging.info('THE GIVEN MODEL: %s'% model_file)
logging.info('LOADING THE MODEL: ')
model = gensim.models.Word2Vec.load(model_file)

listDiff = []
setDiff = []
listX = []
listY = []

# STEP 2 : Getting the vector representation of X and Y X = hyponym Y = hyperny from gold data
leftcount = 0
logging.info('Creating lists from the seed pairs (hyponym, hyponym)')
for i in range(0, countA-1):
    pair = pairITGD[i]
    word1 = re.sub(r'(\S+)=(\S+)', r'\1', pair)
    word2 = re.sub(r'(\S+)=(\S+)', r'\2', pair)
    try:
        x = model[word1]
        y = model[word2]
        listX.append(x)
        listY.append(y)
    except KeyError:
        leftcount = leftcount + 1
        
#print "ORIGINAL PAIRS : %d    ORIGINAL X : %d    ORIGINAL Y : %d  LeftCount : %d" %(countA, len(listX), len(listY), leftcount)
logging.info('The original pairs from the input seed: %d' % countA)
logging.info('The pairs considered for training the PHI: %d' % len(listX))
logging.info('Pairs left out : %d' % leftcount)

phiNSList = []
phiList = []
sumPhiList = []

N = len(listX)

# STEP 3 : phi = vec(Y)/vec(X) - list
logging.info('Calculating the candidate PHI values')
for j in range(0, N-1):
    phiList.append(np.divide(listY[j], listX[j]))

# STEP 4: calculating  right side of equation 1  for each phi in step 3 list.
logging.info('Calculating the arg-min PHI')
for i in range(0, N-1):
    sumV = 0.0000
    tempstr = ""
    for j in range(0, N-1):
        sumV = sumV + computeNormPhiXminYSq(phiList[i], listX[j], listY[j])
    normSum = sumV/N
    sumPhiList.append(normSum)

# STEP 5: Find the phi for whic the result of step 4 is minimum
# with CBOW Model file
# min value of step 4 = 301.364671094
# The PHI for which the value was minimum (arg-min PHI):
'''
[  1.11611132e-02  -1.33015066e-01  -1.23533262e-02  -1.01360762e-02
  -2.49631200e-02  -1.43603921e-01   9.22067184e-03  -2.07354613e-02
   8.46229959e-04  -1.86786409e-02  -1.20678701e-01  -4.20922264e-02
  -6.08642772e-03  -7.24688619e-02   1.38065675e-02   2.55999877e-03
   1.39264120e-02  -5.82282664e-03   7.44669652e-03   3.65147804e-04
   4.90609463e-03   1.67458765e-02   1.63813625e-02  -1.81911252e-02
  -9.14406683e-03   4.13824320e-02   4.01047477e-03   9.64317750e-03
   1.75716002e-02  -5.65313920e-03  -9.77059919e-03  -1.36977937e-02
  -1.06201814e-02   3.99419293e-03  -1.31126288e-02   2.04605330e-03
  -1.84223650e-03  -1.62720662e-02  -1.63770411e-02  -4.83868271e-02
   2.64883297e-03   6.71936432e-03  -5.01118861e-02  -2.08692681e-02
   9.85864364e-03  -4.30306839e-03  -1.77095067e-02   2.05176249e-02
  -5.00700669e-03  -6.32667029e-03  -5.36960829e-03   5.80540225e-02
   8.06472544e-03   5.67688001e-03   4.48960252e-02   4.84122342e-04
  -1.73501857e-02  -2.01555784e-03  -6.76991977e-03  -3.75208980e-03                                  
'''
minPHI = phiList[0]
minRES = sumPhiList[0]
jj = 0

for i in range(1, N-1):
    if sumPhiList[i] < minRES:
        minRES = sumPhiList[i]
        minPHI = phiList[i]
        jj = i

sumPhiList.sort()
logging.info('Minimum Value calculated:')
logging.info(str(minRES))
logging.info('The PHI for which the value was minimum (arg-min PHI):')
logging.info(str(minPHI))

#*******************************************************************************************
#*******************************************************************************************
logging.info('1. APPLYING THE arg-min PHI to the sample data to fetch the hypernyms')
logging.info('   candidates are fetched from : most_similar(positive=[input word vector, PHI VECTOR * input word vector], negative=[]) ')
#*******************************************************************************************
for line in inputF:
    line = re.sub(r'\n',r'',line)
    line = line.lower()
    line = re.sub('concept', '', line)
    line = re.sub('entity', '', line)
    line = re.sub(r'(^\s+)|(\s+$)', r'', line)
    try:
        YVal = minPHI*model[line]                                                  # hypernym vec = PHI * vec(hyponym)
        tempList = model.most_similar(positive=[line,YVal], topn=count)
        tempStr = ''
        for item in tempList:
            vocab , value = item
            tempStr = tempStr + vocab + '\t'
        finalTempStr = GetLookUpWord(tempStr)                                      # Look up in Vocab to refine the hypernym list
        finalTempStr = re.sub(r'(^\s+)|(\s+$)', r'', finalTempStr)
        finalTempStr = re.sub(r'^((\S+\s+){0,15})(\S+\s+)*', r'\1', finalTempStr)  # Get top 15 after refining
        outpuO.write(finalTempStr+'\n')
    except KeyError:
        outpuO.write('\n')
#********************************************************************************************
logging.info('2. APPLYING THE arg-min PHI to the sample data to fetch the hypernyms')
logging.info('   candidates are fetched from : most_similar(positive=[input word vector], negative=[PHI VECTOR * input word vector]) ')
for line in inputF2:
    line = re.sub(r'\n',r'',line)
    line = line.lower()
    line = re.sub('concept', '', line)
    line = re.sub('entity', '', line)
    line = re.sub(r'(^\s+)|(\s+$)', r'', line)
    try:
        YVal = minPHI*model[line]                                                    # hypernym vec = PHI * vec(hyponym)
        tempList = model.most_similar(positive=[line],negative=[YVal], topn=count)
        tempStr = ''
        for item in tempList:
            vocab , value = item
            tempStr = tempStr + vocab + '\t'
        finalTempStr = GetLookUpWord(tempStr)                                        # Look up in Vocab to refine the hypernym list
        finalTempStr = re.sub(r'(^\s+)|(\s+$)', r'', finalTempStr)
        finalTempStr = re.sub(r'^((\S+\s+){0,15})(\S+\s+)*', r'\1', finalTempStr)    # Get top 15 after refining
        outpuO2.write(finalTempStr+'\n')
    except KeyError:
        outpuO2.write('\n')
                                 
inputF.close()
inputF2.close()
