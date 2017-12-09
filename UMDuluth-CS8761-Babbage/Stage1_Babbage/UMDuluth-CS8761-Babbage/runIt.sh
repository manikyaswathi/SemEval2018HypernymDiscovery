#!/bin/bash

# Author : Manikya Swathi Vallabhajosyula
# Creation Date 10/12/2017 9:00:00 P.M.

# This is the main file which executes our system
# OS to execute: UBUNTU 16.04 LTS

#*******************WORKS FOR TRAIL DATA ONLY****************************
#===========================DEFAULT=====================================
# Method : 3 Run the system on mappings of 50 input terms to get candidate hypernyms
# Following are the variables Set for Method 3 RUN leaving rest to default:
# RUN_FROM_START=false
# RUN_ON_SAMPLE=false
# RUN_ON_TRIAL=true
# CREATE_DIC_FILE_NORM=false
# CREATE_RES_FROM_DIC_FILE_NORM=true
# CREATE_DIC_FILE_HEARST=false
# CREATE_RES_FROM_DIC_FILE_HEARST=true
#***************************************************************************
# MODIFY THESE VARIABLES FOR THE SYSTEM TO RUN IN METHOD 2
#**************************************************************************
# Method : 2 Run the system on Normalised text to get candidate hypernyms
# Following are the variables Set for Method 2 RUN leaving rest to default:
# RUN_FROM_START=false
# RUN_ON_SAMPLE=false
# RUN_ON_TRIAL=true
# CREATE_DIC_FILE_NORM=true
# CREATE_RES_FROM_DIC_FILE_NORM=false
# CREATE_DIC_FILE_HEARST=true
# CREATE_RES_FROM_DIC_FILE_HEARST=true
# ------------------------------------------
# DOWNLOAD THE FILES FROM : 	https://drive.google.com/open?id=0B9xD1bj5DY-GUG1raDJzelNvRU0
# ------------------------------------------
# Extract the zip and place in folder : NormText and should look like below
# OUTPUT_DATA_PATH_STORE_H="NormText/DataH"
# OUTPUT_DATA_PATH_STORE_N="NormText/DataN"
#***************************************************************************
# MODIFY THESE VARIABLES FOR THE SYSTEM TO RUN IN METHOD 1
#**************************************************************************
# Method : 1 Run the system on original tagged text to get candidate hypernyms
# Following are the variables Set for Method 1 RUN leaving rest to default:
# RUN_FROM_START=true
# RUN_ON_SAMPLE=false
# RUN_ON_TRIAL=true
# CREATE_DIC_FILE_NORM=true
# CREATE_RES_FROM_DIC_FILE_NORM=false
# CREATE_DIC_FILE_HEARST=true
# CREATE_RES_FROM_DIC_FILE_HEARST=true
# ------------------------------------------
# DOWNLOAD THE FILES FROM : 	https://drive.google.com/file/d/0Bz40_IukD5qDUGVhMURFWE9aYVU/view
# ------------------------------------------
# Extract the zip and place in folder : originalText and should look like below
# OUTPUT_DATA_PATH_H="originalText/DataH"
# OUTPUT_DATA_PATH_N="originalText/DataN"
#****************************************************************************

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$														  $
#$	FOR MORE DETAILS ABOUT VARIABLES OR FORMAT OF INPUT OUPUT FILES LOOK FOR FILE "DetailsOf_runIT_sh.txt"	  $
#$														  $
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# ============MANUAL PRE-PROCESS FILES======================================
# ------Replacing just spaces(not tabs) with an underscore(_)---------------
# e.g.:
# Original Word		|with symbols (Just for Understanding)		|Modified Word				|Type of File
#				(:spc:-space and :tab:-tab) 			
# musical work	music	|musical:spc:work:tab:music			|musical_work	music			|Gold-Data
# musical work 		|musical:spc:work				|musical_work				|Candidate-Vocabulary-Data
# musical work	concept	|musical:spc:work:tab:concept			|musical_work	concept			|Input-Data [Hearts Only]

# ===========RUN MODELS AGAINST : TRIAL or TEST==============================
# RUN_ON_TRIAL=true or false
# set RUN_ON_TRIAL to true to run on trail data
# set RUN_ON_TRIAL to false to run on training data


# We are provided some pre-processed files of Vocabulary and Input FIles
# --------NOT NEEDED FOR NOW------------
# PATH_FOR_VOCABULARY_INPUT="SemEval18-Task9/vocabulary/1A.english.vocabulary.txt"
# PATH_FOR_VOCABULARY_INTERM="SemEval18-Task9/vocabulary/1A.english.vocabulary_0.txt"
# --------NOT NEEDED FOR NOW------------

# The candidate Hypernym words - Needed for METHOD 1,2,3
PATH_FOR_VOCABULARY_OUTPUT="SemEval18-Task9/vocabulary/1A.english.vocabulary_1.txt"

# METHOD 1 Input Parameters
RUN_FROM_START=false
RUN_ON_SAMPLE=false
INPUT_SAMPLE_CORPUS="UMBC_Sample_Corpus/"
INPUT_FULL_COPUS="/home/csgrads/valla045/NLP/UMBC_webbase_all/"

# METHOD 1 Output Parameters
OUTPUT_DATA_PATH_H="temp/DataH/"
OUTPUT_DATA_PATH_N="temp/DataN/"

# METHOD 2 Input Parameters
OUTPUT_DATA_PATH_STORE_H="/home/manikya/Documents/NLP/Babbage/Semval18_T9/temp/preprocessData/DataH/"
OUTPUT_DATA_PATH_STORE_N="/home/manikya/Documents/NLP/Babbage/Semval18_T9/temp/preprocessData/DataN/"

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
# *********************************METHOD 1 pre-processing ENDS***************************************

# Run on TRIAL/TEST
RUN_ON_TRIAL=true

# Hypernym candidate vocabulary file 
VOCAB_TEXT_FILE="SemEval18-Task9/vocabulary/1A.english.vocabulary.under.txt"
# Input terms for which the candidate hypernym words should be fetched from vocabulary

# Input Terms, cooccur & Hearts Patterns, GOLD DATA : for TRIALand TRAINING Data
if $RUN_ON_TRIAL; then
	INPUT_TERM_DATA_N="SemEval18-Task9/trial/data/1A.english.trial.data_N.txt"	# bi/tri grams are separated by space
	INPUT_TERM_DATA_H="SemEval18-Task9/trial/data/1A.english.trial.data_H.txt"	# bi/tri grams are separated by '_'
	INPUT_MAP_DATA_NORM="temp/Maps/1A.english.trial.cooccur.map.txt"
	INPUT_MAP_DATA_HEARST="temp/Maps/1A.english.trial.hearst.map.txt"
	INPUT_GOLD_DATA="SemEval18-Task9/trial/gold/1A.english.trial.gold.txt"
else
	INPUT_TERM_DATA_N="SemEval18-Task9/training/data/1A.english.training.data_N.txt" # bi/tri grams are separated by space
	INPUT_TERM_DATA_H="SemEval18-Task9/training/data/1A.english.training.data_H.txt" # bi/tri grams are separated by '_'
	INPUT_MAP_DATA_NORM="Stemp/Maps/1A.english.train.cooccur.map.txt"
	INPUT_MAP_DATA_HEARST="temp/Maps/1A.english.train.hearst.map.txt"
	INPUT_GOLD_DATA="SemEval18-Task9/training/gold/1A.english.training.gold.txt"
fi

# METHOD 2 Input Parameters - Pattern1
CREATE_DIC_FILE_NORM=false
CREATE_RES_FROM_DIC_FILE_NORM=true


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
CREATE_DIC_FILE_HEARST=false
CREATE_RES_FROM_DIC_FILE_HEARST=true

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

