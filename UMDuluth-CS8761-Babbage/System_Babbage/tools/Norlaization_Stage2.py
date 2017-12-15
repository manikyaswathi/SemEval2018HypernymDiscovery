import os
import re
import time
import nltk
import sys
from stemming.porter2 import stem

# Creating the new normalization data

start_time = time.time()

# @AUTHOR: MANIKYA SWATHI VALLABHAJOSYULA
# PURPOSE : Tools to normalise the input corpus data so that a word embedding matric is built over it
# Run : python Normalization_Stage2.py input_folder/ output_folder/
# NEW NORMALIZATION
# input :
'''
World_NNP War_NNP II_NNP aboard_IN a_DT destroyer_NN escort_NN ._. After_IN the_DT war_NN he_PRP entered_VBD the_DT steel_NN industry_NN and_CC joined_VBD the_DT family_NN owned_VBD Morgan_NNP Construction_NNP Co._NNP ,_, which_WDT creates_VBZ the_DT ``_`` machines_NNS behind_IN the_DT machines_NNS ''_'' --_: designing_VBG continuous_JJ rolling_VBG mills_NNS for_IN worldwide_JJ use_NN ,_, oil-film_JJ bearings_NNS under_IN the_DT name_NN Morgoil_NNP ,_, and_CC universal_JJ joints_NNS and_CC drive_NN spindles_NNS for_IN worldwide_JJ oil-field_NN and_CC rolling-mill_NN applications_NNS ._.
'''
# (a) Intermediate Stage1 Normalized Text:
'''
world war ii destroyer escort war steel industry family morgan construction co.  machines machines mills use bearings name morgoil joints drive spindles oil-field rolling-mill applications   the_name a_destroyer worldwide_oil-field drive_spindles morgan_construction_co. world_war the_war rolling_mills world_war_ii oil-film_bearings the_steel universal_joints morgan_construction the_family oil-field_and_rolling-mill the_ma chines rolling-mill_applications worldwide_use joints_and_drive
'''
# (b) New Normalized Text for Stage 2 final:
'''
world war world_war ii destroyer escort destroyer_escort war entered steel industry steel_industry joined family owned morgan construction morgan_construction co.  machin machin  designing continuous rolling mill worldwide use oil-film bear name morgoil name_morgoil universal joint drive spindl drive_spindl worldwide oil-field rolling-mill applic rolling-mill_applic
'''

# This is done to build word embedding matrix

# list to store popolar POS noun phrase patterns from vocab file
'''
\S+/jj \S+/nn \S+/nn
\S+/rb \S+/nn
\S+/jj \S+/nn
\S+/jj \S+/jj \S+/nn
\S+/nn
\S+/nns \S+/nns
\S+/nns
\S+/vbn \S+/nn
\S+/nn \S+/in \S+/nn
\S+/nn \S+/nn \S+/nn
\S+/nn \S+/nns
\S+/nn \S+/nn
\S+/cd \S+/nn
\S+/nn \S+/jj \S+/nn
\S+/vbg \S+/nn
\S+/dt \S+/nn
\S+/nns \S+/nn
\S+/vb \S+/nn
\S+/jj \S+/nns
\S+/nn \S+/cc \S+/nn
\S+/nn \S+/in \S+/nns
'''
unigramVL = []
bigramVL = []
trigramVL = []

unigramV = []
bigramV = []
trigramV = []

# stemmer = PorterStemmer()

# Function to fetch patterns from vocab_file.txt POS popular tags analysed over the original vocab
def prepPattern():
    singleUn = re.compile(r'(\S+) (\S+)')
    doubleUn = re.compile(r'(\S+) (\S+) (\S+)')
    openf = open("1A.english.vocabulary_1.txt", 'r')
    for line in openf:
        mS = re.match(singleUn, line)
        mD = re.match(doubleUn, line)
        line = re.sub(r'\n', r'', line)
        # Reading each pattern and segregating into respective list
        if mD:
            trigramVL.append(line)
        elif mS:
            bigramVL.append(line)
        else:
            unigramVL.append(line)
# invoking the preparation patterns popular bi-gram and tri-gram patterns from canciadte vocabulary
prepPattern()
# add the all noun bi-gram and tri-gram patterns
trigramVL.append('(\S+/nn[a-z]* \S+/nn[a-z]* \S+/nn[a-z]*)')
bigramVL.append('(\S+/nn[a-z]* \S+/nn[a-z]*)')
trigramV = set(trigramVL)
bigramV = set(bigramVL)
unigramV = set(unigramVL)
biPattern = '('
triPattern = '('

# creating the bigram-pattern from the list of bi-grams to use for re.compile
for val in bigramV:
    biPattern = biPattern + '(' + val + ')' + '|'

# converting all nn to nn[a-z]* patterns to fetch all types of nouns
biPattern = biPattern + 'swathi'
biPattern = re.sub(r'\|swathi', r')', biPattern)
biPattern = re.sub(r'/nn ', r'/nn[a-z]* ', biPattern)
biPattern = re.sub(r'/nn$', r'/nn[a-z]*', biPattern)

# creating the bigram-pattern from the list of bi-grams to use for re.compile
for val in trigramV:
    triPattern = triPattern + '(' + val + ')' + '|'

# converting all nn to nn[a-z]* patterns to fetch all types of nouns
triPattern = triPattern + 'swathi'
triPattern = re.sub(r'\|swathi', r')', triPattern)
triPattern = re.sub(r'/nn ', r'/nn[a-z]* ', triPattern)
triPattern = re.sub(r'/nn$', r'/nn[a-z]*', triPattern)

# compile the bi/tri patterns for re.findall
biPat = re.compile(r'%s' % biPattern)
triPat = re.compile(r'%s' % triPattern)

countE = 0

# NORMALIZE DATA
filepath = sys.argv[1]
ofilepath = sys.argv[2]

# read each file from input folder
for file in os.listdir(filepath):
    if ".possf2" in file:
        # for only possf2 files
        # open the input file
        inputFN = filepath + file
        inputF = open(inputFN, 'r')
        # open the output file
        oFile = re.sub(r'.possf2', r'_Norm.txt', file)
        oFile = ofilepath + oFile
        outputNF = open(oFile, 'w')
        for line in inputF:
            # adding a leading space, converting to lower case and replacing the WORD_TAG to WORD/TAG
            # Done to pattern to apply nltk modules
            Flist = []
            # replace the _ with / between word and POS tag
            # ==================================================================
            #                           NEW NORMALIZATION
            # ==================================================================
            line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
            line = line.lower()                            # convert line to lower case
            tokens = line.split(" ")                       # split for all words
            tokenLine = ""
            for token in tokens:
                # For each token
                # is plural : noun
                # apply stemming and keep the stemmed word , for e.g. cats -> cat
                plural = re.search(r'/nnp?s',token)
                if plural:
                    wordNN = re.sub(r'(\S+)/(\S+)',r'\1',token)
                    wordNT = re.sub(r'(\S+)/(\S+)', r'\2', token)
                    wordTT = stem(wordNN)
                    tokenLine = tokenLine +" "+wordTT+"/"+wordNT
                else:
                    tokenLine = tokenLine + " " + token
            line = tokenLine
            trigrammatch = re.findall(triPat, line, flags=0)  # Find all tri-gram popular POS tags in a line
            list1 = list(nltk.chain(*trigrammatch))           # Converting the tuple to list
            bigrammatch = re.findall(biPat, line, flags=0)    # Find all bi-gram popular POS tags in a line
            list2 = list(nltk.chain(*bigrammatch))            # Converting the tuple to list
            lists = list1 + list2                             # create list of bi-grams and tri-grams  
            listF = list(set(lists))
            # for each bi/tri-gram pattern, fetch its original location and insert the underscored bi/tri-gram.
            # i saw a a beatiful cat with four legs on street -> [a beatiful cat, four legs] -> [Final result]
            # i saw a a beatiful cat a_beautiful_cat beautiful_cat with four legs four_legs on street
            for l in listF:
                try:
                    line = re.sub(l,l+' @SWATHI@',line)
                    l = re.sub(r'(\S+)/[a-z]+( ?)', r'\1\2', l)
                    l = re.sub(r' ', r'_', l)
                    l = l + "/nntb"
                    line = re.sub('@SWATHI@',l, line)
                except:
                    countE = countE + 1
            # strip of new line
            line = re.sub(r'\n', r'', line)
            # removing non - (noun, verb, advern and adjective)
            samline = re.sub(r'((\S+/[^njrv][a-z$]*)( )+)', r'', line)
            # from verbs removing - vbp and vbz
            samline = re.sub(r'((\S+/vb[pz])( )+)', r'', samline)
            # removing rp tags
            samline = re.sub(r'((\S+/rp)( )+)', r'', samline)
            # from adjectives removing jjr and jjs
            samline = re.sub(r'((\S+/jj[rs])( )+)', r'', samline)
            #------------------------------------------------------
            # from the final string, remove the tad annotations
            samline = re.sub(r'/[a-z]+', r'', samline)
            # removing patterns like '/' ./.
            samline = re.sub(r'(\S+)/(\1)', r'', samline)
            # strippping newline and tabs
            samline = re.sub(r'\n', r'', samline)
            samline = re.sub(r'\t+', r'\t', samline)
            # attachinmg a newline to the end of the normalized text
            samline = samline + '\n'
            outputNF.write(samline)

        # close the output file
        outputNF.close()

#print "The EXECUTION TIME is : %s" % (time.time() - start_time)
