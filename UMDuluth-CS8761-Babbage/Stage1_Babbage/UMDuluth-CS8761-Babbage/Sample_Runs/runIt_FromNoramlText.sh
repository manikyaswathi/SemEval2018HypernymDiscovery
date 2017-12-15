#!/bin/bash

# Author : Manikya Swathi Vallabhajosyula
# Creation Date 10/12/2017 9:00:00 P.M.

# This is the main file which executes our system

# ============MANUAL PRE-PROCESS FILES======================================
# ------Replacing just spaces(not tabs) with an underscore(_)---------------
# e.g.:
# Original Word				|with symbols (Just for Understanding)				|Modified Word				|Type of File
#							(:spc:-space and :tab:-tab) 			
# musical work	music		|musical:spc:work:tab:music							|musical_work	music		|Gold-Data
# musical work 				|musical:spc:work									|musical_work				|Candidate-Vocabulary-Data
# musical work	concept		|musical:spc:work:tab:concept						|musical_work	concept		|Input-Data [Hearts Only]

# ===========RUN MODELS AGAINST : TRIAL or TEST==============================
# RUN_ON_TRIAL=true or false
# set RUN_ON_TRIAL to true to run on trail data
# set RUN_ON_TRIAL to false to run on training data

# ***************************************************************************************************************
# ==============Patterns for our system======================================
# PATTERN 1: Bag-of-words cococcurance - per line
# ---------- Example ----------------------------
# INPUT :
# ``_`` The_DT DeLorme_NNP PN-20_NNP represents_VBZ a_DT new_JJ breed_NN of_IN GPS_NNP devices_NNS ._. ..._: a_DT fantastic_JJ device_NN ,_, and_CC it_PRP leads_VBZ the_DT way_NN in_IN a_DT new_JJ breed_NN of_IN GPS_NNP devices_NNS which_WDT can_MD display_VB aerial_JJ photography_NN and_CC satellite_NN imagery_NN ._. For_IN people_NNS who_WP have_VBP dreamed_VBN about_IN having_VBG a_DT Google_NNP Earth_NNP type_NN product_NN in_IN a_DT handheld_JJ device_NN ..._: this_DT is_VBZ it_PRP ._. ''_''
# OUTPUT : bi-gram-trigrams with NN POS tags, unigrams with NN[A-Z]* POS tags
#   delorme pn-20 breed gps devices device way breed gps devices photography satellite imagery people google earth type product device    photography_and_satellite handheld_device new_breed breed_of_gps satellite_imagery aerial_photography the_way the_delorme gps_devices google_earth_type earth_type fantastic_device a_google

# PATTERN 2: Hearsts Patters - with in sentence boundaries
# ---------- Example ----------------------------
# INPUT :
# Those_DT who_WP are_VBP suffering_VBG with_IN this_DT illness_NN have_VBP a_DT low_JJ self-esteem_NN and_CC often_RB a_DT tremendous_JJ need_NN to_TO control_VB their_PRP$ surroundings_NNS and_CC emotions_NNS ._. The_DT Eating_NNP Disorder_NNP ,_, Anorexia_NNP ,_, is_VBZ a_DT unique_JJ reaction_NN to_TO a_DT variety_NN of_IN external_JJ and_CC internal_JJ conflicts_NNS ,_, such_JJ as_IN stress_NN ,_, anxiety_NN ,_, unhappiness_NN and_CC feeling_NN like_IN life_NN is_VBZ out_IN of_IN control_NN ._. 
# OUTPUT : Noun Phrase patters in HEARTS
# internal_conflicts : stress , anxiety , unhappiness , feeling 
# ***************************************************************************************************************

#=======================================================================================
# This system runs in 3 WAYS based on what input data is being used to get the result
#=======================================================================================
#		THIS SYSTEM RUNS METHOD 2
#==================================================================================================================================
# ---------METHOD 2---------------------------
# DESCRIPTION: The basic idea of this process is to read the Normalised Corpus and HEARST patters
# ------------ instead of the entire input corpus (tagged text). [The main difference]
# Then the dictionaries (based on HEARST PATTERNS and co-occurance) for the terms in the 
# trail/training data are built. Later it fetches all the possible matching hypernym terms 
# from the vocabulary of hypernym terms and builds an Output file. 
# The Output file is checked against gold data and is scored.

# INPUT CORPUS : [https://drive.google.com/a/d.umn.edu/file/d/0B9xD1bj5DY-GUG1raDJzelNvRU0/view?usp=sharing]
#---------------

# Parameters to set specific for this RUN:
#---------------------------------
# RUN_FROM_START=false 								[Should be set to false to execute in METHOD 2 or METHOD 3]
# RUN_ON_SAMPLE=false 								[DOES NOT EFFECT THIS RUN]
# INPUT_SAMPLE_CORPUS="UMBC_Sample_Corpus/" 		[DOES NOT EFFECT THIS RUN]
# INPUT_FULL_COPUS="/home/csgrads/valla045/NLP/UMBC_webbase_all/" [DOES NOT EFFECT THIS RUN]
# OUTPUT_DATA_PATH_H="temp/DataH/" 					[Output Path - where the HEARTS ALGORITHM PATTERNS are stored]
# OUTPUT_DATA_PATH_N="temp/DataN/"					[Output Path - where the NORMALISED PATTERNS are stored]
# ***********IMPORTANT TO UPDATE***START************ 
# [https://drive.google.com/a/d.umn.edu/file/d/0B9xD1bj5DY-GUG1raDJzelNvRU0/view?usp=sharing] Parent folder of 'DataN' and 'DataH'
# OUTPUT_DATA_PATH_STORE_N="temp/store/DataN/"		[Since RUN_FROM_START is set to 'false', this path is set to a pre-processed Normalised Input Corpus]
# OUTPUT_DATA_PATH_STORE_H="temp/store/DataH/"		[Since RUN_FROM_START is set to 'false' this path is set to a pre-processed Hearst Patterns]
# ***********IMPORTANT TO UPDATE****END************
# -----For Normalised Patterns----------------
# CREATE_DIC_FILE_NORM=true							[Should be set to true to execute in METHOD 2 and false to execute in METHOD 3]
# CREATE_RES_FROM_DIC_FILE_NORM=false				[Should be set to false to execute in METHOD 2 or and true to execute in METHOD 3]
# INPUT_MAP_DATA_NORM="SemEval18-Task9/vocabulary/1A.english.cooccur.map.txt"		[if CREATE_DIC_FILE_NORM= false & CREATE_RES_FROM_DIC_FILE_NORM=true, then set this path to a pre-generated map file]
# -----For Hearts Patterns----------------
# CREATE_DIC_FILE_HEARST=true							[Should be set to true to execute in METHOD 2 and false to execute in METHOD 3]
# CREATE_RES_FROM_DIC_FILE_HEARST=false					[Should be set to false to execute in METHOD 2 or and true to execute in METHOD 3]
# INPUT_MAP_DATA_HEARST="SemEval18-Task9/vocabulary/1A.english.cooccur.map.txt"		[if CREATE_DIC_FILE_NORM= falsr & CREATE_RES_FROM_DIC_FILE_NORM=true, then set this path to a pre-generated map file]
#==================================================================================================================================
# ---------METHOD 3---------------------------
# DESCRIPTION: The basic idea of this process is to read the pre-build dictionary files
# ------------ built from the Normalised Corpus and HEARST patters instaed of from the 
# entire input corpus or even the Normalised corpus [The main difference]
# THIS OPTION IS PROVIDED TO GET QUICK RESULTS
# This does not work if the input terms (for which the hypernyms should be discovered)
# is changed i.e. modified to anything else apart from trail data. [IMPORTTANT]
# These dictionaries are used to fetch all the possible matching hypernym terms 
# from the vocabulary of hypernym terms and builds an Output file. 
# The Output file is checked against gold data and is scored

# Parameters to set specific for this RUN:
#---------------------------------
# RUN_FROM_START=false 								[Should be set to false to execute in METHOD 2 or METHOD 3]
# RUN_ON_SAMPLE=false 								[DOES NOT EFFECT THIS RUN]
# INPUT_SAMPLE_CORPUS="UMBC_Sample_Corpus/" 		[DOES NOT EFFECT THIS RUN]
# INPUT_FULL_COPUS="/home/csgrads/valla045/NLP/UMBC_webbase_all/" [DOES NOT EFFECT THIS RUN]
# OUTPUT_DATA_PATH_H="temp/DataH/" 					[Output Path - where the HEARTS ALGORITHM PATTERNS are stored]
# OUTPUT_DATA_PATH_N="temp/DataN/"					[Output Path - where the NORMALISED PATTERNS are stored]
# OUTPUT_DATA_PATH_STORE_N="temp/store/DataN/"		[DOES NOT EFFECT THIS RUN]
# OUTPUT_DATA_PATH_STORE_H="temp/store/DataH/"		[DOES NOT EFFECT THIS RUN]
# -----For Normalised Patterns----------------
# CREATE_DIC_FILE_NORM=false						[Should be set to true to execute in METHOD 2 and false to execute in METHOD 3]
# CREATE_RES_FROM_DIC_FILE_NORM=true				[Should be set to false to execute in METHOD 2 or and true to execute in METHOD 3]
# INPUT_MAP_DATA_NORM="SemEval18-Task9/vocabulary/1A.english.cooccur.map.txt"		[IMPORTANT - Stored in the same PATH by DEFAULT]
# [if CREATE_DIC_FILE_NORM= false & CREATE_RES_FROM_DIC_FILE_NORM=true, then set this path to a pre-generated map file of Normalised patterns] 
# -----For Hearts Patterns----------------
# CREATE_DIC_FILE_HEARST=false							[Should be set to true to execute in METHOD 2 and false to execute in METHOD 3]
# CREATE_RES_FROM_DIC_FILE_HEARST=true					[Should be set to false to execute in METHOD 2 or and true to execute in METHOD 3]
# INPUT_MAP_DATA_HEARST="SemEval18-Task9/vocabulary/1A.english.cooccur.map.txt"		[IMPORTANT - Stored in the same PATH by DEFAULT]
# [if CREATE_DIC_FILE_NORM= false & CREATE_RES_FROM_DIC_FILE_NORM=true, then set this path to a pre-generated map file of Hearts patterns]
#====================================================================================
# ------OTHER PARAMS--NOT SPECIFIC TO RUNS-----
# VOCAB_TEXT_FILE="SemEval18-Task9/vocabulary/1A.english.vocabulary.under.txt"  [The modified Vocabulary file with _ instead of spaces]
# INPUT_TERM_DATA_H="SemEval18-Task9/trial/data/1A.english.trial.data_H.txt" or "SemEval18-Task9/training/data/1A.english.training.data_H.txt" [The modified Input Term files with _ instead of spaces for HEARST Algorithm]
# INPUT_TERM_DATA_N="SemEval18-Task9/trial/data/1A.english.trial.data_N.txt" or "SemEval18-Task9/training/data/1A.english.training.data_N.txt" [The modified Input Term files with _ instead of spaces for Cooccurance Algorithm]
# OUTPUT_FILE_DATA_NORM="Output/1A.english.output.norm.txt"						[The Output set of candidate hypernyms created by this system. they are used as keys in scorrer program ]
#=====================================================================================


# We are provided some pre-processed files of Vocabulary and Input FIles
# --------NOT NEEDED FOR NOW------------
# PATH_FOR_VOCABULARY_INPUT="SemEval18-Task9/vocabulary/1A.english.vocabulary.txt"
# PATH_FOR_VOCABULARY_INTERM="SemEval18-Task9/vocabulary/1A.english.vocabulary_0.txt"
# --------NOT NEEDED FOR NOW------------

# The candidate Hypernym words - Needed for METHOD 1,2,3
PATH_FOR_VOCABULARY_OUTPUT="SemEval18-Task9/vocabulary/1A.english.vocabulary_1.txt"

# METHOD 1 Input Parameters
RUN_FROM_START=false				# FALSE for this run
RUN_ON_SAMPLE=true
INPUT_SAMPLE_CORPUS="UMBC_Sample_Corpus/"
INPUT_FULL_COPUS="/home/csgrads/valla045/NLP/UMBC_webbase_all/"

# METHOD 1 Output Parameters
OUTPUT_DATA_PATH_H="temp/DataH/"
OUTPUT_DATA_PATH_N="temp/DataN/"

# METHOD 2 Input Parameters
OUTPUT_DATA_PATH_STORE_H="temp/store/DataH/"
OUTPUT_DATA_PATH_STORE_N="temp/store/DataN/"

# -------------------METHOD 1 PRE PROCESSING-----------------------------------------------------------------
# Step 1: Reads the full Input Corpus
# Step 2: Reads the Vocab POS patterns files
# Step 3: Apply Hearts Algorith - patterns [6 Patterns] and store it in OUTPUT_DATA_PATH_H folder
# Step 4: Uses Pattrens of step 2 to fetch bi-grams and tri-grams of each sentece and append it the sentence
# Step 5: Strip the files of noise - and retaining the bag of words with NN[A-Z]* and bi-gram, trigram patterns
# 		  of the same sentence and store it in a line at OUTPUT_DATA_PATH_N folder.
# ------: each file's normalised patterns and hearts pattern is stores in a separate file 
if $RUN_FROM_START; then
   echo "Extracting patterns and Normalising the corpus for Information from vocabulary: "
   # Setting the input corpus to actual vs sample corpus
   if $RUN_ON_SAMPLE; then
      INPUT_CORPUS=$INPUT_SAMPLE_CORPUS
   else
      INPUT_CORPUS=$INPUT_FULL_COPUS
   fi
   echo "Extracting patterns of vocab type from SAMPLE CORPUS "
   now=$(date +"%T")
   echo "Start time : $now" >> LOG.txt
   echo "Start time : $now"
   # Executing the pattern exctraction program on 5 types of files in parallel
   #Sample run HearstAlgo_Norm.py "Pre-processed candidate-vocab.txt File" "Input Full Corpus Folder" "Output file path for Pre-processed patterns" "file type - one out of 5"
   python src/HearstAlgo_Norm.py $PATH_FOR_VOCABULARY_OUTPUT $INPUT_CORPUS $OUTPUT_DATA_PATH_H $OUTPUT_DATA_PATH_N "delorme.com_shu.pages_" >> LOG.txt &
   python src/HearstAlgo_Norm.py $PATH_FOR_VOCABULARY_OUTPUT $INPUT_CORPUS $OUTPUT_DATA_PATH_H $OUTPUT_DATA_PATH_N "mbta.com_mtu.pages_" >> LOG.txt &
   python src/HearstAlgo_Norm.py $PATH_FOR_VOCABULARY_OUTPUT $INPUT_CORPUS $OUTPUT_DATA_PATH_H $OUTPUT_DATA_PATH_N "ucdavis_wnba.pages_" >> LOG.txt &
   python src/HearstAlgo_Norm.py $PATH_FOR_VOCABULARY_OUTPUT $INPUT_CORPUS $OUTPUT_DATA_PATH_H $OUTPUT_DATA_PATH_N "utexas_iit.pages_" >> LOG.txt &
   python src/HearstAlgo_Norm.py $PATH_FOR_VOCABULARY_OUTPUT $INPUT_CORPUS $OUTPUT_DATA_PATH_H $OUTPUT_DATA_PATH_N "weather.yahoo_bbk.ac.pages_" >> LOG.txt &
   wait
   now=$(date +"%T")
   echo "completion time : $now"
   echo "Completiontime time : $now" >> LOG.txt
else
   # The input corpus is changed to pre-processed corpus for Method 2 or 3
   OUTPUT_DATA_PATH_H=$OUTPUT_DATA_PATH_STORE_H
   OUTPUT_DATA_PATH_N=$OUTPUT_DATA_PATH_STORE_N
   echo "FILES ALREADY EXIST IN THE STORE PATH $OUTPUT_DATA_PATH_STORE_H and $OUTPUT_DATA_PATH_STORE_N"
   echo "FILES ALREADY EXIST IN THE STORE PATH $OUTPUT_DATA_PATH_STORE_H and $OUTPUT_DATA_PATH_STORE_N" >> LOG.txt
fi

# Run on TRIAL/TEST
RUN_ON_TRIAL=true

# Hypernym candidate vocabulary file 
VOCAB_TEXT_FILE="SemEval18-Task9/vocabulary/1A.english.vocabulary.under.txt"
# Input terms for which the candidate hypernym words should be fetched from vocabulary

# Input Terms, cooccur & Hearts Patterns, GOLD DATA : for TRIALand TRAINING Data
if $RUN_ON_TRIAL; then
	INPUT_TERM_DATA_N="SemEval18-Task9/trial/data/1A.english.trial.data_N.txt"
	INPUT_TERM_DATA_H="SemEval18-Task9/trial/data/1A.english.trial.data_H.txt"
	INPUT_MAP_DATA_NORM="temp/Maps/1A.english.trial.cooccur.map.txt"
	INPUT_MAP_DATA_HEARST="temp/Maps/1A.english.trial.hearst.map.txt"
	INPUT_GOLD_DATA="SemEval18-Task9/trial/gold/1A.english.trial.gold.txt"
else
	INPUT_TERM_DATA_N="SemEval18-Task9/training/data/1A.english.training.data_N.txt"
	INPUT_TERM_DATA_H="SemEval18-Task9/training/data/1A.english.training.data_H.txt"
	INPUT_MAP_DATA_NORM="Stemp/Maps/1A.english.train.cooccur.map.txt"
	INPUT_MAP_DATA_HEARST="temp/Maps/1A.english.train.hearst.map.txt"
	INPUT_GOLD_DATA="SemEval18-Task9/training/gold/1A.english.training.gold.txt"
fi

# METHOD 2 Input Parameters - Pattern1
CREATE_DIC_FILE_NORM=true		# TRUE for this run
CREATE_RES_FROM_DIC_FILE_NORM=false	# FALSE for this run


# METHOD 2,3 OUTPUT Parameters- Pattern1
if $RUN_ON_TRIAL; then
	OUTPUT_FILE_DATA_NORM="Output/1A.english.output.trial.norm.txt"
else
	OUTPUT_FILE_DATA_NORM="Output/1A.english.output.train.norm.txt"
fi

# ------------------PATTERN 1 : NORMALISED BAG OF WORDS----CO-OCCURANCE----------------------
# -------------------METHOD 1, METHOD 2, METHOD 3------------------------------------------------------
# ---------METHOD 2 CREATING RESULTS AFTER BUILDING DICTIONARIES FROM PRE-PROCESSED DATA---------------
# ----------------METHOD 3 CREATING RESULTS FROM PRE-PROCESSED DICTIONARY FILES------------------------
# Step 1: If METHOD 2  			generate_candidate_from_corpus.py 
# 		  Step 1.1: Read the Normalised pattern files
#		  Step 1.2: Create the map of Input Terms vs Co-occurance terms with counts
#         Step 1.3: Create the output file with candidate hypernyms by mapping the co-occurance words to 
#					candiadte hypernym vocabulary file and rank them
# Step 2: If METHOD 3  			generate_candidate_load_map.py
# 		  Step 1.1: Read the pre-generated mapping file : input term(the trail/training data) to co-occurance with rank
#         Step 1.2: Create the output file with candidate hypernyms by mapping the co-occurance words to 
#					candiadte hypernym vocabulary file and rank them
if $CREATE_DIC_FILE_NORM; then
	# METHOD 2
	now=$(date +"%T")
	echo "GENERATING OUTPUT FROM NORMALISED TEXT AT TIME $now" >> LOG.txt
	#Sample run generate_candidate_from_corpus.py "input-term.txt file" "Pre-processed Corpus Folder" "input-candidate-vocab.txt File" "output.txt File"
	python src/generate_candidate_from_corpus.py $INPUT_TERM_DATA_N $OUTPUT_DATA_PATH_N $VOCAB_TEXT_FILE $OUTPUT_FILE_DATA_NORM
	now=$(date +"%T")
	echo "COMPLETE : GENERATED OUTPUT FROM NORMALISED TEXT AT TIME $now" >> LOG.txt
else
	if $CREATE_RES_FROM_DIC_FILE_NORM; then
		# METHOD 3
		now=$(date +"%T")
		echo "GENERATING OUTPUT FROM PRE PROCESSED DICTIONARY AT TIME $now" >> LOG.txt
		#Sample run generate_candidate_from_corpus.py "input-term.txt file" "Pre-generated map File" "input-candidate-vocab.txt File" "output.txt File"
		python src/generate_candidate_load_map.py $INPUT_TERM_DATA_N $INPUT_MAP_DATA_NORM $VOCAB_TEXT_FILE $OUTPUT_FILE_DATA_NORM
		now=$(date +"%T")
		echo "COMPLETE : GENERATED OUTPUT FROM PRE PROCESSED DICTIONARY AT TIME $now" >> LOG.txt
	fi
	wait
fi

# ------------------PATTERN 2 : HEARST PATTERNS-------------------------------------------------------
# -------------------METHOD 1, METHOD 2, METHOD 3------------------------------------------------------
# ---------METHOD 2 CREATING RESULTS AFTER BUILDING DICTIONARIES FROM PRE-PROCESSED DATA---------------
# ----------------METHOD 3 CREATING RESULTS FROM PRE-PROCESSED DICTIONARY FILES------------------------
# Step 1: If METHOD 2  			hearst_generate_candidate_from_corpus.py
# 		  Step 1.1: Read the Hearst pattern files
#		  Step 1.2: Create the map of Input Terms(hyponym) vs hypernym terms (candidates) with counts
#         Step 1.3: Create the output file with candidate hypernyms by mapping the candidate hypernym terms to 
#					candiadte hypernym vocabulary file and rank them
# Step 2: If METHOD 3  			hearst_generate_candidate_load_map.py
# 		  Step 1.1: Read the pre-generated mapping file : input term(the trail/training data) to candidate hypernym with rank
#		  Step 1.2: Create the output file with candidate hypernyms by mapping the candidate hypernym terms to 
#					candiadte hypernym vocabulary file and rank them

# METHOD 2 Input Parameters - Pattern2
CREATE_DIC_FILE_HEARST=true		# TRUE for this run
CREATE_RES_FROM_DIC_FILE_HEARST=false	# FALSE for this run

# METHOD 2,3 Output Parameters - Pattern2
if $RUN_ON_TRIAL; then
	OUTPUT_FILE_DATA_HEARST="Output/1A.english.output.trial.hearst.txt"
else
	OUTPUT_FILE_DATA_HEARST="Output/1A.english.output.train.hearst.txt"
fi


if $CREATE_DIC_FILE_HEARST; then
	now=$(date +"%T")
	echo "GENERATING OUTPUT FROM HEARST TEXT AT TIME $now" >> LOG.txt
	#Sample run hearst_generate_candidate_from_corpus.py "input-term.txt file" "Pre-processed Corpus Folder" "input-candidate-vocab.txt File" "output.txt File"
	python src/hearst_generate_candidate_from_corpus.py $INPUT_TERM_DATA_H $OUTPUT_DATA_PATH_H $VOCAB_TEXT_FILE $OUTPUT_FILE_DATA_HEARST
	now=$(date +"%T")
	echo "COMPLETE : GENERATED OUTPUT FROM NORMALISED TEXT AT TIME $now" >> LOG.txt
else
	if $CREATE_RES_FROM_DIC_FILE_HEARST; then
		now=$(date +"%T")
		echo "GENERATING OUTPUT FROM PRE PROCESSED DICTIONARY HEARST AT TIME $now" >> LOG.txt
		#Sample run hearst_generate_candidate_from_corpus.py "input-term.txt file" "Pre-generated map File" "input-candidate-vocab.txt File" "output.txt File"
		python src/hearst_generate_candidate_load_map.py $INPUT_TERM_DATA_H $INPUT_MAP_DATA_HEARST $VOCAB_TEXT_FILE $OUTPUT_FILE_DATA_HEARST
		now=$(date +"%T")
		echo "COMPLETE : GENERATED OUTPUT FROM PRE PROCESSED DICTIONARY HEARST AT TIME $now" >> LOG.txt
	fi
	wait
fi


# =========================================================================================
#                        SCORING MODULE
# =========================================================================================
echo "*******************************************************************" >> RESULTS.TXT
echo "*****************RESULTS FROM CO-OCCURANCE ONLY***************" >> RESULTS.TXT
echo "*******************************************************************" >> RESULTS.TXT

python SemEval18-Task9/task9-scorer.py $INPUT_GOLD_DATA $OUTPUT_FILE_DATA_NORM >> RESULTS.TXT

echo "*******************************************************************" >> RESULTS.TXT
echo "*****************RESULTS FROM HEARST ONLY***************" >> RESULTS.TXT
echo "*******************************************************************" >> RESULTS.TXT

python SemEval18-Task9/task9-scorer.py $INPUT_GOLD_DATA $OUTPUT_FILE_DATA_HEARST >> RESULTS.TXT

if $RUN_ON_TRIAL; then
	OUTPUT_FILE_DATA_MERGE="Output/1A.english.output.trial.merge.txt"
else
	OUTPUT_FILE_DATA_MERGE="Output/1A.english.output.train.merge.txt"
fi

python src/mergeOutput.py $OUTPUT_FILE_DATA_NORM $OUTPUT_FILE_DATA_HEARST $OUTPUT_FILE_DATA_MERGE

echo "*******************************************************************" >> RESULTS.TXT
echo "*****************RESULTS FROM Pattern1 and Pattern2****************" >> RESULTS.TXT
echo "*******************************************************************" >> RESULTS.TXT

python SemEval18-Task9/task9-scorer.py $INPUT_GOLD_DATA $OUTPUT_FILE_DATA_MERGE >> RESULTS.TXT

