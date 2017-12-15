import os
import re
import time
import sys
import nltk
from stemming.porter2 import stem

# Creating new Hearst Patterns

start_time = time.time()
# @AUTHOR: MANIKYA SWATHI VALLABHAJOSYULA
# PURPOSE : Tools to normalise the Hearst Patterns of stage 1 (All 6 mention in Swathi_stage2_report) so that a word embedding matric is built over it
# Run : python Hearts_Patterns_Stage2_Norm_6.py input_folder/ output_folder/
# input : cars such as bmw, audi
# intermediate result (stage1): cars : bmw , audi
# new normalised result : cars bmw cars audi cars

# THis is done to give more weights to hearst pattern in word embeddings


'''
---------------------------HEARTS PATTERNS-------------------------------
Hearst Patterns : http://people.ischool.berkeley.edu/~hearst/papers/coling92.pdf
=========================================================================
NP : Noun Phrase - <DT>? <JJ|VB[A-Z]>? <NN[A-Z]>
COND : <,>? <CC>?
=========================================================================
No.     Pattern                   :       Example
---   -----------                       ------------
HP1. NP such as (NP COND)* NP     :   NP such as NP   [or]    NP such as NP, NP and NP
HP2. such NP as (NP COND)* NP     :   NP such as NP   [or]    NP such as NP, NP and NP
HP3. NP (COND NP)* and other NP   :   NP and other NP [or]    NP, NP and other NP
HP4. NP (COND NP)* or other NP    :   NP or other NP  [or]    NP, NP or other NP
HP5. NP including (NP COND)* NP   :   NP including NP  [or]   NP including NP, NP
HP6. NP especially (NP COND)* NP   :   NP especially NP  [or]   NP especially NP, NP
-------------Pattern and Hyper-Hypo relationship-------------------------
No.         hyper-pypo pattern
----    ----------------------------
HP1. <Hypernym> such as <Hyponym List>
HP2. such <Hypernym> as <Hyponym List>
HP3. <Hyponym List> and other <Hypernym>
HP4. <Hyponym List> or other <Hypernym>
HP5. <Hypernym> including <Hyponym List>
HP6. such <Hypernym> especially <Hyponym List>
'''


start_time = time.time()

# NORMALIZE HEARTS
filepath = sys.argv[1]               # folder path for input UMBC_webbase_sample corpus
ofilepath = sys.argv[2]               # folder path to store the normalised results
# The pattersn to match the above hearst patterns
such_tags = re.compile(r' such/jj ') 
suchas_tags = re.compile(r' such/jj as/in ')
orOther_tags = re.compile(r' (?:(?:or)|(?:and))/cc other/jj ')
andOther_tags = re.compile(r' and/cc other/jj ')
ines_tags = re.compile(r' (?:including|especially)/[a-z]+ ')

'''
The following approach is applied in creating the EACH normalised Hearst patterns:
For each hearst pattern (1..6):
       1. The pattern phrase with the pattern is extracted from input line
       2. The stage 1 result is obtained by appling STEP 2 (below) # PATTERN 1 - STAGE 1 = hypernym : hyponym list                                   3. the stage 2 result is obtained by applying STEP 3 (below)# PATTERN 2 - STAGE 2 = hypernym hyponym1 hypernym hyponym2 hypernym ...   end         
***************REGULAR EXPRESSION PATTERNS USED IN THIS FILE*******************************
STEP 1: These patterns are used at mutlple locations in this program: to match Hearst Patterns (6)
----------------------------------------------------------------------------------------------------------------------------
1. (\S+) (\S+)                                      :   Pattern to match two words separated by a space
2. (\S+) (\S+) (\S+)                                :   Pattern to match three words separated by a space each
3. (\S+/nn[a-z]* \S+/nn[a-z]* \S+/nn[a-z]*)         :   Patterns like NN NN NN, NN NNS NNP, NNP NNP NNP and so on
4. (\S+/nn[a-z]* \S+/nn[a-z]*)                      :   Patterns like NN NN, NN NNP, NNP NNP and so on
5. (?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))?
                                                    :   Patterns like dt jj nn [or] dt jj nn nn and [or] .....
6. (?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *)+
                                                    :   Patterns like dt jj nn and [or] vb nn nn , [or] ....
7. (?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+
                                                    :   Patterns like , and dt jj nn [or] and vb nn [or] ....
8.  (?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+
                                                    :   Patterns like dt jj nn [or] nn nn [or] ....
9.  (?:(?:,/, *)(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+)+
                                                    :   Patterns like , dt jj nn [or] dt nnp nnp [or] ....
10. (?:,/, )?(?:(?:and)|(?:or))/cc other/jj         :   Patterns like , and other [or] or other [or] ....
11. (?:,_, )?(?:and|or)/[a-z]+                      :   Patterns like , and [or] or [or] ...
12. (?:-lrb-/-lrb- )(?:including|excluding)/[a-z]+ :   Patterns like -lrb- including [or] -lrb- excluding [HAVE TO BE MODIFIED]
13. ' ?%s ?%s (?:\S+/[^-][a-z]* )+-rrb-/-rrb-'      :   Patterns like abc xyz .... -rrb-
================================================================================================================================
STEP 2: Formatting the STEP 1 HP patterns to <Hypernym> : <Hyponym List> pattern  STAGE 1
--------------------------------------------------------------------------------------------------------------------------------
1.  formItem = re.sub(r' +', r'_', item)                    :   replace (spaces) with (_)
2.  formItem = re.sub(r'(_such_as_)',r' : ', formItem)      :   replacing (_such_as_) with ( : )
3.  formItem = re.sub(r'(_,) : ', r' : ', formItem)         :   replacing (_, : ) with ( : )
4.  formItem = re.sub(r'(_,_)(and|or)_', r' , ', formItem)  :   replacing (_,_and_) [or] (_,_or_) with ( , )
5.  formItem = re.sub(r'_,_', r' , ', formItem)             :   replacing (_,_) with ( , )
6.  formItem = re.sub(r'_(and|or)_', r' , ', formItem)      :   replacing (_(and|or)_) with ( , )
7.  formItem = re.sub(r'_$', r'', formItem)                 :   replacing (_$) with ()
8.  formItem = re.sub(r'(\\/[a-zA-Z0-9]+_)', r'_', formItem):   replacing (\\/[a-zA-Z0-9]+_) with (_) [e.g. 'car/bike transport' to 'car_transport'
=================================================================================================================================
STEP 3: Re-Formatting the stage 1 HP patterns from <Hypernym> : <Hyponym List> pattern to <hypernym> <hyponym1> <hypernym> <hyponym2>..
for STAGE 2 embeddings
----------------------------------------------------------------------------------------------------------------------------------
1: hhSep = formItem.strip().split("=")                        : extracting the hypernym and list of hyponyms
2: formItem = re.sub(r',', ', '+hhSep[0]+',', formItem)       : inserting hypernyms between hyponyms i.e. at the , location      
3: formItem = re.sub(r'$', ' , ' + hhSep[0] + ', ', formItem) : inserting hyeprnym at the end
4: formItem = re.sub(r'=', ',', formItem)                     : replacing the hypernym separation = with ,
5: formItem = re.sub(r'^', r' ', formItem)                    : add space at begining
6: formItem = re.sub(r'( (\S+/\S+_)+(\S+/\S+)_(\S+/\S+)_(\S+/\S+) ,)', r' \3_\4_\5 ,', formItem)
                                                              : replacing n-gram with its tri-gram noun phrase
7: formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                                                              : replacing tri-gram with its tri-gram and back-off unigram noun phrase
8. formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3_\4 ,', formItem)
                                                              : replacing tri-gram with its tri-gram and back-off bigram noun phrase
7. formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                                                              : replacing bi-gram with its bi-gram and back-off unigram noun phrase
8. formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3 ,', formItem)
                                                              : replacing bi-gram with its bi-gram and back-off unigram noun phrase
9. formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)\1', r'\1', formItem)
                                                              : remocing duplicated values
10.formItem = re.sub(r'_', r' ', formItem)                    : replace back the spaces
11. formItemL = re.split(r'(?:,/, )?(?:(?:and/[a-z]+)|(?:or/[a-z]+)) +other/[a-z]+ ', item)
    formItem = formItemL[1] + '='+formItemL[0]
                                                              : reformatting <hyponym list> : <hypernym> as <hypernym> : <hyponym list>
12.Few other formatiings done to remove unwanted chanractes from the reulsting string
                        formItem = re.sub(r' , $', r'', formItem)
                        formItem = re.sub(r'(\S+)/(\S+)', r'\1', formItem)
                        formItem = re.sub(r'^ ', r'', formItem)
                        formItem = re.sub(r' ', r'_', formItem)
                        formItem = re.sub(r'_,_', r' ', formItem)
'''
# for each file in input folder:
for file in os.listdir(filepath):
    if ".possf2" in file:
        # only for possf2 files
        inputFN = filepath + file
        inputF = open(inputFN, 'r')
        oFile = re.sub(r'.possf2', r'_HA.txt', file)
        oFile = ofilepath + oFile
        outputHF = open(oFile, 'w')
        # for each line in input file
        for line in inputF:
            line = " "+line
            line = line.lower()
            line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
            matchsuch = re.search(such_tags, line)
            matchsuchas = re.search(suchas_tags, line)
            matchorOther = re.search(orOther_tags, line)
            matchAndOther = re.search(andOther_tags, line)
            matchInEs = re.search(ines_tags, line)
            if matchsuch:
                # FOr match with "MATCH SUCH"
                # 1 pattern: NP0 such as NP1, NP2 , ...., (and|or)? NPn
                #                     OR
                # 2 pattern: such NP0 as NP1, NP2 , ...., (and|or)? NPn
                # np is pattern for NP0
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))?'
                # np2 and lsep are patterns for NP1..n
                np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *)+'
                lsep = '(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+'
                if matchsuchas:
                    # for pattern match "SUCH AS" : 1 pattern
                    cc = '(?:(?:and)|(?:or))'
                    # get the pattern match
                    pattern = re.compile(r'%s such/jj as/in (?:%s )?%s' % (np, np2, lsep))
                    npTuple = re.findall(pattern, line, flags=0)
                    for item in npTuple:
                        # PATTERN 1 - STAGE 1 = hypernym : hyponym list
                        formItem = re.sub(r' +', r'_', item)
                        formItem = re.sub(r'(_such/[a-z]+_as/[a-z]+_)', r' = ', formItem)
                        formItem = re.sub(r'(_,/,) = ', r' = ', formItem)
                        formItem = re.sub(r'(_,/,_)(and/[a-z]+|or/[a-z]+)_', r' , ', formItem)
                        formItem = re.sub(r'_,/,_', r' , ', formItem)
                        formItem = re.sub(r'_(and/[a-z]+|or/[a-z]+)_', r' , ', formItem)
                        formItem = re.sub(r'_$', r'', formItem)
                        formItem = re.sub(r'(\\/[a-zA-Z0-9]+/[a-z]+_)', r'_', formItem)
                        # PATTERN 2 - STAGE 2 = hypernym hyponym1 hypernym hyponym2 hypernym ...
                        hhSep = formItem.strip().split("=")
                        formItem = re.sub(r',', ', '+hhSep[0]+',', formItem)
                        formItem = re.sub(r'$', ' , ' + hhSep[0] + ', ', formItem)
                        formItem = re.sub(r'=', ',', formItem)
                        formItem = re.sub(r'^', r' ', formItem)
                        formItem = re.sub(r'( (\S+/\S+_)+(\S+/\S+)_(\S+/\S+)_(\S+/\S+) ,)', r' \3_\4_\5 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3_\4 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)\1', r'\1', formItem)
                        formItem = re.sub(r'_', r' ', formItem)
                        formItem = re.sub(r' , $', r'', formItem)
                        formItem = re.sub(r'(\S+)/(\S+)', r'\1', formItem)
                        formItem = re.sub(r'^ ', r'', formItem)
                        formItem = re.sub(r' ', r'_', formItem)
                        formItem = re.sub(r'_,_', r' ', formItem)
                        # writing to output file
                        outputHF.write('%s \n' % formItem)
                else:
                    # For match with "MATCH NP SUCH"
                    # 2 pattern: such NP0 as NP1, NP2 , ...., (and|or)? NPn
                    # np is pattern for NP0                                  
                    pattern = re.compile(r' such/jj %s as/in (?:%s )?%s' % (np, np2, lsep))
                    npTuple = re.findall(pattern, line, flags=0)
                    for item in npTuple:
                        # PATTERN 1 - STAGE 1 = hypernym : hyponym list
                        formItem = re.sub(r' such/jj (%s) as/in ' % np, r'\1 = ', item)
                        formItem = re.sub(r' +', r'_', formItem)
                        formItem = re.sub(r'(_,/,)?_=_', r' = ', formItem)
                        formItem = re.sub(r'(_,/,_)((and/[a-z]+)|(or/[a-z]+))_', r' , ', formItem)
                        formItem = re.sub(r'_,/,_', r' , ', formItem)
                        formItem = re.sub(r'_((and/[a-z]+)|(or/[a-z]+))_', r' , ', formItem)
                        formItem = re.sub(r'_$', r'', formItem)
                        formItem = re.sub(r'(\\/[a-zA-Z0-9]+_)', r'_', formItem)
                        # PATTERN 2 - STAGE 2 = hypernym hyponym1 hypernym hyponym2 hypernym ... 
                        hhSep = formItem.strip().split("=")
                        formItem = re.sub(r',', ', ' + hhSep[0] + ',', formItem)
                        formItem = re.sub(r'$', ' , ' + hhSep[0] + ', ', formItem)
                        formItem = re.sub(r'=', ',', formItem)
                        formItem = re.sub(r'^', r' ', formItem)
                        formItem = re.sub(r'( (\S+/\S+_)+(\S+/\S+)_(\S+/\S+)_(\S+/\S+) ,)', r' \3_\4_\5 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3_\4 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)\1', r'\1', formItem)
                        formItem = re.sub(r'_', r' ', formItem)
                        formItem = re.sub(r' , $', r'', formItem)
                        formItem = re.sub(r'(\S+)/(\S+)', r'\1', formItem)
                        formItem = re.sub(r'^ ', r'', formItem)
                        formItem = re.sub(r' ', r'_', formItem)
                        formItem = re.sub(r'_,_', r' ', formItem)
                        # Write to output file
                        outputHF.write('%s \n' % formItem)
            if matchorOther:
                # 3, 4 pattern : match pattern NP1, NP2, ..., NPn (and|or) other NP0
                # np and np2 for NP1, Np2, ..., NPn patterns
                # np is also used for NP0 pattern
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+'
                np2 = '(?:(?:,/, *)(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+)+'
                # pattern : (or|and) other 
                oao = '(?:,/, )?(?:(?:and)|(?:or))/cc other/jj'
                pattern = re.compile(r' %s(?:%s )?%s %s' % (np, np2, oao, np))
                npTuple = re.findall(pattern, line, flags=0)
                for item in npTuple:
                    # PATTERN 1 - STAGE 1 = hypernym : hyponym list
                    formItemL = re.split(r'(?:,/, )?(?:(?:and/[a-z]+)|(?:or/[a-z]+)) +other/[a-z]+ ', item)
                    formItem = formItemL[1] + '='+formItemL[0]
                    formItem = re.sub(r' +', r'_', formItem)
                    formItem = re.sub(r'(_,/,)?_=_', r' = ', formItem)
                    formItem = re.sub(r'(_,/,_)((and/[a-z]+)|(or/[a-z]+))_', r' , ', formItem)
                    formItem = re.sub(r'_,/,_', r' , ', formItem)
                    formItem = re.sub(r'_((and/[a-z]+)|(or/[a-z]+))_', r' , ', formItem)
                    formItem = re.sub(r'_$', r'', formItem)
                    formItem = re.sub(r'(\\/[a-zA-Z0-9]+_)', r'_', formItem)
                    # PATTERN 2 - STAGE 2 = hypernym hyponym1 hypernym hyponym2 hypernym ...  
                    hhSep = formItem.strip().split("=")
                    formItem = re.sub(r',', ', ' + hhSep[0] + ',', formItem)
                    formItem = re.sub(r'$', ' , ' + hhSep[0] + ', ', formItem)
                    formItem = re.sub(r'=', ',', formItem)
                    formItem = re.sub(r'^', r' ', formItem)
                    formItem = re.sub(r'( (\S+/\S+_)+(\S+/\S+)_(\S+/\S+)_(\S+/\S+) ,)', r' \3_\4_\5 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3_\4 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)\1', r'\1', formItem)
                    formItem = re.sub(r'_', r' ', formItem)
                    formItem = re.sub(r' , $', r'', formItem)
                    formItem = re.sub(r'(\S+)/(\S+)', r'\1', formItem)
                    formItem = re.sub(r'^ ', r'', formItem)
                    formItem = re.sub(r' ', r'_', formItem)
                    formItem = re.sub(r'_,_', r' ', formItem)
                    # write to the output file
                    outputHF.write('%s \n' % formItem)
            if matchInEs:
                # 5, 6 patterns :  NP0 (especially|including)  NP1, NP2, ....,(and|or)? NPn
                # np : used in NP1,2,..,n and NP0
                # np2 : used in NP1,2,..,n
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+'
                np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:,/, *)?)+'
                np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:,/, *)|(?:(?:and|or)/cc *))?)+'
                # match (and|or)
                oao = '(?:,_, )?(?:and|or)/[a-z]+'
                matchlrp = re.search(r' -lrb-/-lrb- ', line)
                if matchlrp:
                    # MATCH -lrb--rrb- whcih also has patterns
                    cie = '(?:-lrb-/-lrb- )(?:including|excluding)/[a-z]+'
                    pattern = re.compile(r' ?%s ?%s (?:\S+/[^-][a-z]* )+-rrb-/-rrb-' % (np, cie))
                    npTuple = re.findall(pattern, line, flags=0)
                    for item in npTuple:
                        # PATTERN 1 - STAGE 1 = hypernym : hyponym list
                        formItem = re.sub(r' -lrb-/-lrb- (?:(?:including/[a-z]+)|(?:excluding/[a-z]+)) ', r' = ', item)
                        formItem = re.sub(r'-rrb-/-rrb-', r'', formItem)
                        formItem = re.sub(r' +', r'_', formItem)
                        formItem = re.sub(r'(_,/,)?_=_', r' = ', formItem)
                        formItem = re.sub(r'(_,/,_)((and/[a-z]+)|(or/[a-z]+))_', r' , ', formItem)
                        formItem = re.sub(r'_,/,_', r' , ', formItem)
                        formItem = re.sub(r'_((and/[a-z]+)|(or/[a-z]+))_', r' , ', formItem)
                        formItem = re.sub(r'^_|_$', r'', formItem)
                        formItem = re.sub(r'((\\/[a-zA-Z0-9]+)+_)', r'_', formItem)
                        # PATTERN 2 - STAGE 2 = hypernym hyponym1 hypernym hyponym2 hypernym ...  
                        hhSep = formItem.strip().split("=")
                        formItem = re.sub(r',', ', ' + hhSep[0] + ',', formItem)
                        formItem = re.sub(r'$', ' , ' + hhSep[0] + ', ', formItem)
                        formItem = re.sub(r'=', ',', formItem)
                        formItem = re.sub(r'^', r' ', formItem)
                        formItem = re.sub(r'( (\S+/\S+_)+(\S+/\S+)_(\S+/\S+)_(\S+/\S+) ,)', r' \3_\4_\5 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3_\4 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3 ,', formItem)
                        formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)\1', r'\1', formItem)
                        formItem = re.sub(r'_', r' ', formItem)
                        formItem = re.sub(r' , $', r'', formItem)
                        formItem = re.sub(r'(\S+)/(\S+)', r'\1', formItem)
                        formItem = re.sub(r'^ ', r'', formItem)
                        formItem = re.sub(r' ', r'_', formItem)
                        formItem = re.sub(r'_,_', r' ', formItem)
                        # write to output file
                        outputHF.write('%s \n' % formItem)
                        # outputFN4.write('%s \n' % formItem)
                # Getting the patterns 5 and 6 from whcih are outside -lrb- -rrb- ( )
                # excluding and including patterns
                cie = '(?:,/, )?(?:including|excluding)/[a-z]+'
                pattern = re.compile(r' %s ?%s (?:%s)* ?(?:%s)? ?%s' % (np, cie, np2, oao, np))
                npTuple = re.findall(pattern, line, flags=0)
                for item in npTuple:
                    # PATTERN 1 - STAGE 1 = hypernym : hyponym list
                    formItem = re.sub(r' (?:,/, )?(?:(?:including/[a-z]+)|(?:excluding/[a-z]+)) ', r' = ', item)
                    formItem = re.sub(r' +', r'_', formItem)
                    formItem = re.sub(r'(_,/,)?_=_', r' = ', formItem)
                    formItem = re.sub(r'(_,/,_)((and/[a-z]+)|(or/[a-z]+))_', r' , ', formItem)
                    formItem = re.sub(r'_,/,_', r' , ', formItem)
                    formItem = re.sub(r'_((and/[a-z]+)|(or/[a-z]+))_', r' , ', formItem)
                    formItem = re.sub(r'^_|_$', r'', formItem)
                    formItem = re.sub(r'((\\/[a-zA-Z0-9]+)+_)', r'_', formItem)
                    # PATTERN 2 - STAGE 2 = hypernym hyponym1 hypernym hyponym2 hypernym ...
                    hhSep = formItem.strip().split("=")
                    formItem = re.sub(r',', ', ' + hhSep[0] + ',', formItem)
                    formItem = re.sub(r'$', ' , ' + hhSep[0] + ', ', formItem)
                    formItem = re.sub(r'=', ',', formItem)
                    formItem = re.sub(r'^', r' ', formItem)
                    formItem = re.sub(r'( (\S+/\S+_)+(\S+/\S+)_(\S+/\S+)_(\S+/\S+) ,)', r' \3_\4_\5 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3_\4 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/nn[a-z]*)_(\S+/nn[a-z]*) ,)', r'\1 \2 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)', r'\1 \3 ,', formItem)
                    formItem = re.sub(r'( ([\w-]+/[a-z]+)_(\S+/[a-z]+) ,)\1', r'\1', formItem)
                    formItem = re.sub(r'_', r' ', formItem)
                    formItem = re.sub(r' , $', r'', formItem)
                    formItem = re.sub(r'(\S+)/(\S+)', r'\1', formItem)
                    formItem = re.sub(r'^ ', r'', formItem)
                    formItem = re.sub(r' ', r'_', formItem)
                    formItem = re.sub(r'_,_', r' ', formItem)
                    # Writing result to output file
                    outputHF.write('%s \n' % formItem)
        # Closing the output file
        outputHF.close()

#print "The EXECUTION TIME is : %s" % (time.time() - start_time)
