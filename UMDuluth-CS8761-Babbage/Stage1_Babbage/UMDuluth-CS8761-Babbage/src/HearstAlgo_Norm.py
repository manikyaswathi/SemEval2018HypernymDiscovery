"""
Created on Thu Oct 10 07:35:10 2017

Author: Manilkya Swathi Vallabhajosyula
Team Babbage : CS 8761 Project
SemEval-2018 Task 9: Hypernym Discovery

Purpose : Create two patterns files - Normalied Cooccurance & Hearst Patterns
References:
1. Co-occurance on Bag of Words : https://arxiv.org/pdf/1603.08702.pdf
2. Hearst Patterns : http://people.ischool.berkeley.edu/~hearst/papers/coling92.pdf

How to execute:
python HearstAlgo_Norm.py vocab_file.txt UMBC_Webbase_all_Coprus_PATH Output_File_Hearst_Path Output_File_cooccur_Path pattern_of_file_name

Where:
> vocab_file.txt           :   The vocabulary file with top patterns. [ Location : Stage1SV18T9/SemEval18-Task9/vocabulary/ Usage File:1A.english.vocabulary_1.txt original File:1A.english.vocabulary.txt ]
> UMBC_Webbase_all_Coprus_PATH   :   The original UMBC folder (408 files of 5 types) with tagged corpus [ https://drive.google.com/file/d/0Bz40_IukD5qDUGVhMURFWE9aYVU/view ]
> Output_File_Hearst_Path  :   The output path to store the Hearst Patterns extracted from the UMBC corpus
> Output_File_cooccur_Path :   The output path to store the normalised texts extracted from the UMBC corpus
> pattern_of_file_name     :   There are 5 pattern of files names and this specifies which files a thread picks up
[ delorme.com_shu.pages_, mbta.com_mtu.pages_, ucdavis_wnba.pages_, utexas_iit.pages_, weather.yahoo_bbk.ac.pages_ ]

e.g. :
python HearstAlgo_Norm.py ../SemEval18-Task9/vocabulary/1A.english.vocabulary.under.txt ../NLP/UMBC_webbase_all ../temp/DataH ../temp/DataN "delorme.com_shu.pages_" &

& at the end runs the process in the background, helps to execute multple normalisers at once.

Functions:
----------
prepPattern : fetches the POS tag patterns from 'vocab_file.txt' and stores in uni/bi/tri-gram pattern lists

---------------------------HEARTS PATTERNS-------------------------------
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

**************************************************************************************************************
e.g. files
**********1A.english.vocabulary_1.txt****************
\S+/jj \S+/nn \S+/nn
\S+/rb \S+/nn
..............
..............
\S+/nn \S+/cc \S+/nn
\S+/nn \S+/in \S+/nns
**********DATA FROM UBMC Corpus: a few lined from file : delorme.com_shu.pages_11.possf2***************
Each_DT participant_NN in_IN Lazzaro_NNP 's_POS research_NN study_NN was_VBD asked_VBN to_TO play_VB their_PRP$ favorite_JJ video_NN games_NNS -_: games_NNS that_WDT ranged_VBD from_IN action_NN titles_NNS like_IN Halo_NNP and_CC Grand_NNP Theft_NN Auto_NN 3_CD to_TO puzzle_VB games_NNS such_JJ as_IN Tetris_NNP and_CC Snood_NNP -_: while_IN cameras_NNS recorded_VBD their_PRP$ facial_JJ expressions_NNS ._. Lazzaro_NNP then_RB analyzed_VBD players_NNS '_POS reactions_NNS to_TO the_DT games_NNS on_IN a_DT moment-by-moment_JJ basis_NN ._.

UK_NNP games_NNS developer_NN ._. he_PRP has_VBZ previously_RB contributed_VBN to_TO a_DT number_NN of_IN UK_NNP computer_NN magazines_NNS ,_, and_CC was_VBD the_DT co-editor_NN of_IN www.videogamedesign.com_NN ,_, scooping_VBG interviews_NNS with_IN such_JJ greats_NNS as_IN Chris_NNP Crawford_NNP and_CC Peter_NNP Molyneux_NNP ._.

Imagine_VB a_DT place_NN where_WRB gamers_NNS throng_VBP ._. Where_WRB ,_, every_DT day_NN of_IN the_DT week_NN ,_, every_DT hour_NN of_IN the_DT day_NN ,_, hundreds_NNS or_CC even_RB thousands_NNS go_VBP head-to-head_RB ._. Imagine_VB these_DT online_JJ revelers_NNS proudly_RB unveiling_VBG their_PRP$ custom-created_JJ levels_NNS ,_, synergistically_RB sharing_VBG techniques_NNS and_CC game_NN secrets_NNS ,_, and_CC uncontrollably_RB increasing_VBG their_PRP$ game-addiction_NN ._. Imagine_VB the_DT previews_NNS of_IN your_PRP$ sequel_NN that_IN they_PRP 'll_MD see_VB and_CC the_DT shopping_NN galleries_NNS where_WRB they_PRP can_MD purchase_VB new_JJ levels_NNS ,_, new_JJ titles_NNS ,_, t-shirts_NNS ,_, and_CC other_JJ goodies_NNS directly_RB from_IN you_PRP ._. These_DT are_VBP some_DT of_IN the_DT possibilities_NNS of_IN bringing_VBG video_NN games_NNS online_VBP ._.

You_PRP probably_RB decided_VBD at_IN a_DT very_RB early_JJ stage_NN whether_IN your_PRP$ game_NN will_MD be_VB a_DT short-duration_NN game_NN or_CC an_DT eternal\/persistent_JJ game_NN ._. However_RB ,_, keep_VB in_IN mind_NN that_IN eternal\/persistent_JJ games_NNS may_MD require_VB more_JJR maintenance_NN -LRB-_-LRB- in_IN particular_JJ ,_, server_NN maintenance_NN -RRB-_-RRB- than_IN short-duration_NN games_NNS and_CC have_VBP the_DT additional_JJ requirement_NN of_IN coping_VBG gracefully_RB with_IN power_NN failures_NNS ,_, crashes_NNS ,_, or_CC other_JJ interruptions_NNS of_IN service_NN ._.

``_`` how_WRB much_JJ does_VBZ it_PRP cost_NN ''_'' ,_, and_CC ``_`` who_WP pays_VBZ for_IN it_PRP ?_. ''_'' Pricing_NN depends_VBZ on_IN many_JJ factors_NNS and_CC will_MD vary_VB from_IN one_CD provider_NN to_TO another_DT ,_, but_CC the_DT range_NN is_VBZ from_IN 12-16_CD %_NN of_IN the_DT costs_NNS of_IN development_NN ._. This_DT covers_VBZ the_DT bond_NN fee_NN and_CC the_DT bank_NN charges_NNS ,_, including_VBG interest_NN ._. In_IN most_JJS instances_NNS ,_, the_DT costs_NNS of_IN the_DT bond\/bank_JJ financing_NN are_VBP added_VBN into_IN the_DT price_NN paid_VBN by_IN the_DT publisher_NN upon_IN delivery_NN and_CC are_VBP included_VBN in_IN the_DT bank_NN loan_NN ._. Therefore_RB ,_, the_DT developer_NN is_VBZ not_RB out_IN of_IN pocket_NN for_IN the_DT costs_NNS ,_, but_CC does_VBZ not_RB start_VB earning_VBG royalties_NNS until_IN the_DT costs_NNS are_VBP recouped_VBN by_IN the_DT publisher_NN ._.

Also_RB ,_, you_PRP ca_MD n't_RB always_RB escape_VB bank_NN holidays_NNS ._. Some_DT countries_NNS -LRB-_-LRB- especially_RB Catholic_JJ countries_NNS -RRB-_-RRB- shut_VBP down_RP totally_RB for_IN a_DT couple_NN of_IN days_NNS once_RB or_CC twice_RB a_DT year_NN -LRB-_-LRB- same_JJ for_IN Japan_NNP in_IN May_NNP -RRB-_-RRB- :_: should_MD you_PRP need_VB them_PRP to_TO open_VB office_NN for_IN you_PRP ,_, let_VB them_PRP know_VB in_IN advance_NN ._.

****************************************************************
Intermediate Patterns: [Each a differnt pattern of 6 patterns] [Read - Hearts Patterns Structure of ReadMe.txt]
----------------------
> puzzle_VB games_NNS such_JJ as_IN Tetris_NNP and_CC Snood_NNP
> such_JJ greats_NNS as_IN Chris_NNP Crawford_NNP and_CC Peter_NNP Molyneux_NNP
> new_JJ levels_NNS ,_, new_JJ titles_NNS ,_, t-shirts_NNS ,_, and_CC other_JJ goodies_NNS
> power_NN failures_NNS ,_, crashes_NNS ,_, or_CC other_JJ interruptions_NNS
> the_DT bank_NN charges_NNS ,_, including_VBG interest_NN
> countries_NNS -LRB-_-LRB- especially_RB Catholic_JJ countries_NNS -RRB-_-RRB-
****************************************************************
                    [STEP A] Pattern 1
*********Hearts Pattern file for the above line*****************
Hypernym            :  Hyponym
----------------------------------------------------------------
puzzle games        :  Tetris, Snood
greats              :  Chris Crawford, Peter Molyneux
goodies             :  new levels, new titlesn t-shirts
interruptions       :  power failures, crashes
the_bank_charges    :  interest
countries           :  Catholic_countires

***********Intermediate patters for normalization************
The POS tag patterns from 'vocab_file.txt' matching with the input string
Either the bigram or trigram patters are noted and appended tp the end of line.
-----------------------------------------------------------------------------
Step 1: LOOK FOR PATTERNS : NNS IN NNP, JJ NNS, NN IN NNP, NN NNS, ....
Each_DT participant_NN in_IN Lazzaro_NNP 's_POS research_NN study_NN was_VBD asked_VBN to_TO play_VB their_PRP$ favorite_JJ video_NN games_NNS -_: games_NNS that_WDT ranged_VBD from_IN action_NN titles_NNS like_IN Halo_NNP and_CC Grand_NNP Theft_NN Auto_NN 3_CD to_TO puzzle_VB games_NNS such_JJ as_IN Tetris_NNP and_CC Snood_NNP -_: while_IN cameras_NNS recorded_VBD their_PRP$ facial_JJ expressions_NNS ._. Lazzaro_NNP then_RB analyzed_VBD players_NNS '_POS reactions_NNS to_TO the_DT games_NNS on_IN a_DT moment-by-moment_JJ basis_NN ._.
Step 2: listing the The matching Bi/Tri-grams are
titles_like_halo, facial_expressions, participant_in_lazzaro, action_titles, ....
Step 3: strip the files of non-noun words and remove tags
participant lazzaro research study video games games action titles halo grand theft auto games tetris snood cameras expressions lazzaro players reactions games basis
Step 4: Append the Step 3 with the list of strings of Step 2 to get the following: [Final Normalised Text]
participant lazzaro research study video games games action titles halo grand theft auto games tetris snood cameras expressions lazzaro players reactions games basis   titles_like_halo facial_expressions participant_in_lazzaro action_titles moment-by-moment_basis tetris_and_snood grand_theft puzzle_games favorite_video_games the_games research_study grand_theft_auto each_participant favorite_video
*************************************************************************************
                    [STEP B] Pattern 2
***************Normalied Texts of original above lines*******************************
participant lazzaro research study video games games action titles halo grand theft auto games tetris snood cameras expressions lazzaro players reactions games basis   titles_like_halo facial_expressions participant_in_lazzaro action_titles moment-by-moment_basis tetris_and_snood grand_theft puzzle_games favorite_video_games the_games research_study grand_theft_auto each_participant favorite_video

uk games developer number uk computer magazines co-editor www.videogamedesign.com interviews greats chris crawford peter molyneux   a_number such_greats chris_crawford peter_molyneux number_of_uk uk_computer uk_games_developer the_co-editor crawford_and_peter uk_games co-editor_of_www.videogamedesign.com scooping_interviews greats_as_chris

place gamers day week hour day hundreds thousands revelers levels techniques game secrets game-addiction previews sequel shopping galleries levels titles t-shirts goodies possibilities video games   even_thousands every_day sharing_techniques online_revelers a_place bringing_video game_secrets the_day new_titles the_shopping the_previews new_levels custom-created_levels techniques_and_game the_week other_goodies every_hour the_possibilities

stage game short-duration game game mind games maintenance  server maintenance  short-duration games requirement power failures crashes interruptions service   early_stage interruptions_of_service eternal\_games server_maintenance additional_requirement power_failures short-duration_games other_interruptions a_short-duration eternal\_game

cost    pricing factors provider range % costs development bond fee bank charges interest instances costs financing price publisher delivery bank loan developer pocket costs royalties costs publisher   many_factors publisher_upon_delivery including_interest the_price earning_royalties the_developer the_bank the_range the_costs 12-16_% the_bond one_provider costs_of_development the_publisher bond\_financing

 bank holidays countries  countries  couple days year  japan may  office advance   a_year catholic_countries some_countries a_couple japan_in_may escape_bank open_office couple_of_days

**************************************************************************************************
[STEP A] and [STEP B] Apllied on all lines of all files in UMBC_webbase_all Files to get the pre prcessed DATA
**************************************************************************************************
**********************REGULAR EXPRESSION PATTERNS USED IN THIS FILE*******************************
These patterns are used at mutlple locations in this program:
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

---Formatting the HP patterns to <Hypernym> : <Hyponym List> pattern-------
1.  formItem = re.sub(r' +', r'_', item)                    :   replace (spaces) with (_)
2.  formItem = re.sub(r'(_such_as_)',r' : ', formItem)      :   replacing (_such_as_) with ( : )
3.  formItem = re.sub(r'(_,) : ', r' : ', formItem)         :   replacing (_, : ) with ( : )
4.  formItem = re.sub(r'(_,_)(and|or)_', r' , ', formItem)  :   replacing (_,_and_) [or] (_,_or_) with ( , )
5.  formItem = re.sub(r'_,_', r' , ', formItem)             :   replacing (_,_) with ( , )
6.  formItem = re.sub(r'_(and|or)_', r' , ', formItem)      :   replacing (_(and|or)_) with ( , )
7.  formItem = re.sub(r'_$', r'', formItem)                 :   replacing (_$) with ()
8.  formItem = re.sub(r'(\\/[a-zA-Z0-9]+_)', r'_', formItem):   replacing (\\/[a-zA-Z0-9]+_) with (_) [e.g. 'car/bike transport' to 'car_transport'


  Pattern----ReplacePattern
1. r'/nn '----r'/nn[a-z]* '
"""

# list of imports
import os
import re
import time
import sys
import nltk

start_time = time.time()

# Lists and sets to store the top unigram, bigram and tri gram patterns
unigramVL = []
bigramVL = []
trigramVL = []
unigramV = []
bigramV = []
trigramV = []

# Mandates the process to start with at least 5 files
argcount = len(sys.argv)
if argcount < 6:
    print "Insufficient params for processing CORPUS\n"
    sys.exit()

# Setting up filenames from arguments
vocabFilePath = sys.argv[1]
corpusFilePath = sys.argv[2]
outputFilePathH = sys.argv[3]
outputFilePathN = sys.argv[4]
specificFile = sys.argv[5]


# Function to fetch patterns from vocab_file.txt POS popular tags analysed over the original vocab
def prepPattern():
    singleUn = re.compile(r'(\S+) (\S+)')
    doubleUn = re.compile(r'(\S+) (\S+) (\S+)')
    openf = open(vocabFilePath, 'r')
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
    openf.close()


# Fetching the existing popular POS tag patterns
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

# creating the trigram-pattern from the list of bi-grams to use for re.compile
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

# Key Search Phrases for Hearts Algorithm Patterns
# As in HEARTS PATTERS [ABOVE]
such_tags = re.compile(r' such/jj ')
suchas_tags = re.compile(r' such/jj as/in ')
orOther_tags = re.compile(r' (?:(?:or)|(?:and))/cc other/jj ')
andOther_tags = re.compile(r' and/cc other/jj ')
ines_tags = re.compile(r' (?:including|especially)/[a-z]+ ')

# Reading each file from the UMBC_webbase_all corpus to create Pattern1 and Pattern2 files [STEP A] and [STEP B]
for file in os.listdir(corpusFilePath):
    # Since filenames with one perticular pattern are processed by one process of this program, this helps opening
    # files files which are just required by a process
    if specificFile in file:
        # opening the tagged input File
        inputFN = corpusFilePath + file
        inputF = open(inputFN, 'r')
        # opening the output file for STEP A
        oFile = re.sub(r'.possf2', r'_HA.txt', file)
        oFile = outputFilePathH + oFile
        outputHF = open(oFile, 'w')
        # opening the output file for STEP B
        oFile = re.sub(r'.possf2', r'_Norm.txt', file)
        oFile = outputFilePathN + oFile
        outputNF = open(oFile, 'w')
        # for each line from a selected file
        for line in inputF:
            # adding a leading space, converting to lower case and replacing the WORD_TAG to WORD/TAG
            # Done to pattern to apply nltk modules
            line = " " + line
            line = line.lower()
            line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
            # ==================================================================
            #                           [STEP A]
            # ==================================================================
            # For a given line look for all possible Hearst Pattern
            matchsuch = re.search(such_tags, line)  # HP2
            matchsuchas = re.search(suchas_tags, line)  # HP1
            matchorOther = re.search(orOther_tags, line)  # HP4
            matchAndOther = re.search(andOther_tags, line)  # HP3
            matchInEs = re.search(ines_tags, line)  # HP5, HP6
            if matchsuch:
                # Either HP1 or HP2 [explained above]
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))?'
                np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *)+'
                lsep = '(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+'
                if matchsuchas:
                    # Either HP1
                    cc = '(?:(?:and)|(?:or))'
                    # the below is building pattern HP1
                    pattern = re.compile(r'%s such/jj as/in (?:%s )?%s' % (np, np2, lsep))
                    # fetching all HP1 patterns
                    npTuple = re.findall(pattern, line, flags=0)
                    for item in npTuple:
                        # Eliminate the tags
                        item = re.sub(r'(\S+)/(\S+)', r'\1', item)
                        # normalising to HP patters [Explained above]
                        formItem = re.sub(r' +', r'_', item)
                        formItem = re.sub(r'(_such_as_)', r' : ', formItem)
                        formItem = re.sub(r'(_,) : ', r' : ', formItem)
                        formItem = re.sub(r'(_,_)(and|or)_', r' , ', formItem)
                        formItem = re.sub(r'_,_', r' , ', formItem)
                        formItem = re.sub(r'_(and|or)_', r' , ', formItem)
                        formItem = re.sub(r'_$', r'', formItem)
                        formItem = re.sub(r'(\\/[a-zA-Z0-9]+_)', r'_', formItem)
                        outputHF.write('%s \n' % formItem)
                else:
                    # HP2 Pattern
                    pattern = re.compile(r' such/jj %s as/in (?:%s )?%s' % (np, np2, lsep))
                    # fetching all HP2 patterns
                    npTuple = re.findall(pattern, line, flags=0)
                    for item in npTuple:
                        # forming 'such <NP> as' to '<NP>:'
                        formItem = re.sub(r' such/jj (%s) as/in ' % np, r'\1 : ', item)
                        # Eliminate the tags
                        formItem = re.sub(r'(\S+)/(\S+)', r'\1', formItem)
                        # normalising to HP patters [Explained above]
                        formItem = re.sub(r' +', r'_', formItem)
                        formItem = re.sub(r'(_,)?_:_', r' : ', formItem)
                        formItem = re.sub(r'(_,_)(and|or)_', r' , ', formItem)
                        formItem = re.sub(r'_,_', r' , ', formItem)
                        formItem = re.sub(r'_(and|or)_', r' , ', formItem)
                        formItem = re.sub(r'_$', r'', formItem)
                        formItem = re.sub(r'(\\/[a-zA-Z0-9]+_)', r'_', formItem)
                        outputHF.write('%s \n' % formItem)
            if matchorOther:
                # Pattern HP3 and HP4 [explained above]
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+'
                np2 = '(?:(?:,/, *)(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+)+'
                oao = '(?:,/, )?(?:(?:and)|(?:or))/cc other/jj'
                pattern = re.compile(r' %s(?:%s )?%s %s' % (np, np2, oao, np))
                # get all HP3 and HP4 patterns
                npTuple = re.findall(pattern, line, flags=0)
                for item in npTuple:
                    # Eliminate the tags
                    item = re.sub(r'(\S+)/(\S+)', r'\1', item)
                    # Split the string at 'and other' or 'or other' to bring the hypernym to front of formation
                    formItemL = re.split(r'(?:, )?(?:and|or) +other ', item)
                    formItem = formItemL[1] + ':' + formItemL[0]
                    # normalising to HP patters [Explained above]
                    formItem = re.sub(r' +', r'_', formItem)
                    formItem = re.sub(r'(_,)?_:_', r' : ', formItem)
                    formItem = re.sub(r'(_,_)(and|or)_', r' , ', formItem)
                    formItem = re.sub(r'_,_', r' , ', formItem)
                    formItem = re.sub(r'_(and|or)_', r' , ', formItem)
                    formItem = re.sub(r'_$', r'', formItem)
                    formItem = re.sub(r'(\\/[a-zA-Z0-9]+_)', r'_', formItem)
                    outputHF.write('%s \n' % formItem)
            if matchInEs:
                # Pattern HP5 or HP6
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+'
                np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:,/, *)?)+'
                np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:,/, *)|(?:(?:and|or)/cc *))?)+'
                oao = '(?:,_, )?(?:and|or)/[a-z]+'
                # match left bracket
                matchlrp = re.search(r' -lrb-/-lrb- ', line)
                if matchlrp:
                    # match patterns <NP> -lrb- including|especially ........... -rrb-
                    cie = '(?:-lrb-/-lrb- )(?:including|excluding)/[a-z]+'
                    pattern = re.compile(r' ?%s ?%s (?:\S+/[^-][a-z]* )+-rrb-/-rrb-' % (np, cie))
                    npTuple = re.findall(pattern, line, flags=0)
                    for item in npTuple:
                        # removing all POS tags
                        item = re.sub(r'(\S+)/(\S+)', r'\1', item)
                        formItem = re.sub(r' -lrb- (?:including|excluding) ', r' : ', item)
                        # normalising to HP patters [Explained above]
                        formItem = re.sub(r'-rrb-', r'', formItem)
                        formItem = re.sub(r' +', r'_', formItem)
                        formItem = re.sub(r'(_,)?_:_', r' : ', formItem)
                        formItem = re.sub(r'(_,_)(and|or)_', r' , ', formItem)
                        formItem = re.sub(r'_,_', r' , ', formItem)
                        formItem = re.sub(r'_(and|or)_', r' , ', formItem)
                        formItem = re.sub(r'^_|_$', r'', formItem)
                        formItem = re.sub(r'((\\/[a-zA-Z0-9]+)+_)', r'_', formItem)
                        outputHF.write('%s \n' % formItem)
                # matching original HP5 and HP6 without -lrb- ..... -rrb- patterns
                cie = '(?:,/, )?(?:including|excluding)/[a-z]+'
                pattern = re.compile(r' %s ?%s (?:%s)* ?(?:%s)? ?%s' % (np, cie, np2, oao, np))
                npTuple = re.findall(pattern, line, flags=0)
                for item in npTuple:
                    # Removing tags
                    item = re.sub(r'(\S+)/(\S+)', r'\1', item)
                    formItem = re.sub(r' (?:, )?(?:including|excluding) ', r' : ', item)
                    # normalising to HP patters [Explained above]
                    formItem = re.sub(r' +', r'_', formItem)
                    formItem = re.sub(r'(_,)?_:_', r' : ', formItem)
                    formItem = re.sub(r'(_,_)(and|or)_', r' , ', formItem)
                    formItem = re.sub(r'_,_', r' , ', formItem)
                    formItem = re.sub(r'_(and|or)_', r' , ', formItem)
                    formItem = re.sub(r'^_|_$', r'', formItem)
                    formItem = re.sub(r'((\\/[a-zA-Z0-9]+)+_)', r'_', formItem)
                    outputHF.write('%s \n' % formItem)
            # ==================================================================
            #                           [STEP A]
            # ==================================================================
            Flist = []
            # convert _ to / : for nltk modules (if used any)
            line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
            line = line.lower()                         # convert to lower case
            unLine = line
            trigrammatch = re.findall(triPat, line, flags=0)    # Find all tri-gram popular POS tags in a line
            list1 = list(nltk.chain(*trigrammatch))             # Converting the tuple to list
            bigrammatch = re.findall(biPat, line, flags=0)      # Find all bi-gram popular POS tags in a line
            list2 = list(nltk.chain(*bigrammatch))              # Converting the tuple to list
            lists = list1 + list2                               # creating one bi/tri-gram lists
            listF = list(set(lists))                            # removing duplicates
            listFF = []
            for l in listF:
                l = re.sub(r'(\S+)/[a-z]+( ?)', r'\1\2', l)     # Pull POS tags out
                l = re.sub(r' ', r'_', l)                       # convert bi/trigrams from space sep to _ sep
                # e.g. 'hello world' to 'hello_world'
                l = l + "/nntb"                                 # append a joint tag 'nntb' so that this could not be pulled out in STOP list later
                listFF.append(l)
            linen = " ".join(listFF)
            line = line + " " + linen                           # Appending the bigram and trigram data to the line
            samline = re.sub(r'((\S+/[^n][a-z$]*)( )+)', r'', line) # Remove all non /nn[a-z]* tags - STOP tags
            samline = re.sub(r'/[a-z]+', r'', samline)          # Remove the POS tags
            samline = re.sub(r'(\S+)/(\1)', r'', samline)       # remove POS tags like word e.g. -lrb-/-lrb- to -lrb
            samline = re.sub(r'\n', r'', samline)               # removing all intermittent new lines
            samline = samline + '\n'                            # add only one new line at the end
            outputNF.write(samline)                             # writing to the file
        inputF.close()
        outputHF.close()
        outputNF.close()

print "The EXECUTION TIME for files starting with %s is : %s" % (specificFile, time.time() - start_time)
