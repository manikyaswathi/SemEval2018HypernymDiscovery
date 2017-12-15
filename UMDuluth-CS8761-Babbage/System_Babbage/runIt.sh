#!/bin/sh

#Author : Manikya Swathi Vallabhajosyula
# Purpose: Execute our Sytem_Babbage and mergers results and evaluates scores


# Two Types of Runs: WITH CBOW WORD EBMEDDING
# 1. TRIAL DATA
# 2. TRAINING DATA
# THE ABOVE TWO COULD ALSO BE REPEASTED FOR Skip-gram but the result is inconsistant and poor.

# Since te COPURS, THE PATTERNS and THE EEMBEDDINGS ARE CONSTANT for english task, we are directly building results on the embeddings and patterns than geenrating them first.

# Run 1: CBOW + TRAINING DATA [DEFAULT] Takes close to 2 hours on akka
# RUN_ON_TRAIN=true
# RUN_ON_TRIAL=false
# CBOW_MODEL=true
# Run 2: CBOW + TRAINING DATA - Takes close to 1:15 hours on akka
# RUN_ON_TRAIN=false
# RUN_ON_TRIAL=true
# CBOW_MODEL=true
# ---------------------------------------------------------------------------------------------
# COULD KEEP REST ALL VARIABLES UNCHANGED
# ---------------------------------------------------------------------------------------------
# If desired, can cahnge the OUTPUT_DIR names. But other wise, we create backup with time stamp
# ==== For Skip-Gram =============
# Run 1: Skip-gram + TRAINING DATA [DEFAULT] Takes close to 2 hours on akka
# RUN_ON_TRAIN=true
# RUN_ON_TRIAL=false
# CBOW_MODEL=false
# Run 2: kip-gram + TRAINING DATA - Takes close to 1:15 hours on akka
# RUN_ON_TRAIN=false
# RUN_ON_TRIAL=true
# CBOW_MODEL=false

echo "Please Ignore remove warnings"


RUN_ON_TRAIN=true
RUN_ON_TRIAL=false
CBOW_MODEL=true

# DO Not mof=dify OUTPUT_MAIN
OUTPUT_MAIN=Output

# Setting default name of output Directory based on trial vs training
if $RUN_ON_TRAIN; then
    OUTPUT_DIR=TRAINING
else
    OUTPUT_DIR=TRIAL
fi

# Getting stage 1 results base on trial vs training
if $RUN_ON_TRAIN; then
    STAGE1_NORM="1A.english.output.train.norm.txt"
    STAGE1_HEARST="1A.english.output.train.hearst.txt"
else
    STAGE1_NORM="1A.english.output.trial.norm.txt"
    STAGE1_HEARST="1A.english.output.trial.hearst.txt"
fi

STAGE2_MODEL1="src/BuildModel1"
# Getting stage 2 Model1 results based on trial vs training
if $RUN_ON_TRAIN; then
    MODEL1="Stage2_Model1_train.txt"
else
    MODEL1="Stage2_Model1_trial.txt"
fi

STAGE2_PHIMOD="src/PHIModule"
# Getting stage 2 PHIModule results based on trial vs training
if $RUN_ON_TRAIN; then
    PHI1="Stage2_Phi01_train.txt"
    PHI2="Stage2_Phi02_train.txt"
else
    PHI1="Stage2_Phi01_trial.txt"
    PHI2="Stage2_Phi02_trial.txt"
fi

MERGE_MOD="src/Merge"

# a copy of the training and trial data is places in each of the folders
# Getting input data based on trial vs training
if $RUN_ON_TRAIN; then
    DATA="1A.english.training.data.txt"
else
    DATA="1A.english.trial.data.txt"
fi

# assigning the Gold Data File
# Getting gold data based on trial vs training
if $RUN_ON_TRAIN; then
    GOLD="1A.english.training.gold.txt"
else
    GOLD="1A.english.trial.gold.txt"
fi

# OPUTPUT DIRECTORY
cd $OUTPUT_MAIN
if [ -d "$OUTPUT_DIR" ]; then
    timestamp=`date '+%d_%m_%Y_%H_%M_%S'`
    NEW_OP_DIR=${OUTPUT_DIR}_$timestamp
    mkdir $NEW_OP_DIR
    cp $OUTPUT_DIR/* $NEW_OP_DIR/ 
    rm -R $OUTPUT_DIR
fi
cd ../

# Running Stage 2 Module 1
cd $STAGE2_MODEL1
rm $MODEL1
touch $MODEL1
./prepareNew.sh $DATA $MODEL1
cp $MODEL1 ../Merge/
cp Model1.LOG ../Merge/Model1.LOG

cd ../../

#echo "ONE DONE"
# Running Stage 2 PHI Module
cd $STAGE2_PHIMOD

if $CBOW_MODEL; then
    EMBEDDING="UMBCNewNormNoStopHearst_CBOW_20_10"
else
    EMBEDDING="UMBCNewNormNoStopHearst_SG_20_10"
fi
rm $PHI1 $PHI2
touch $PHI1 $PHI2
python PhiModule.py $EMBEDDING $DATA $PHI1 $PHI2
cp $PHI1 ../Merge/
cp $PHI2 ../Merge/
cp Model2.LOG ../Merge/Model2.LOG

cd ../../

#echo "Two Done"

# Running Merge Module with op files
cd $MERGE_MOD

./runMergeEval.sh $OUTPUT_DIR $STAGE1_NORM $STAGE1_HEARST $MODEL1 $PHI1 $PHI2 $GOLD $DATA

#echo "THREE DONE"

# Copying logs to putput folder and deleting few files
cp Model1.LOG $OUTPUT_DIR
cp Model2.LOG $OUTPUT_DIR
rm Model1.LOG
rm Model2.LOG
rm $PHI1 $PHI2 $MODEL1
rm $OUTPUT_DIR/mergeTwoResults.py
rm $OUTPUT_DIR/SeparateCEOp.py
rm $OUTPUT_DIR/SeparateCEOp.py
rm $OUTPUT_DIR/task9-scorer.py
rm $OUTPUT_DIR/MergeResults.sh
cp -R $OUTPUT_DIR ../../$OUTPUT_MAIN/

cd ../../

# copying the main result to the System_Babbage folder
timestamp=`date '+%d_%m_%Y_%H_%M_%S'`
RES_REPORT=Results_${OUTPUT_DIR}_$timestamp
echo " SYSTEM_BABBAGE FINAL RESULTS " > $RES_REPORT
cat $OUTPUT_MAIN/$OUTPUT_DIR/Evaluation_Report.LOG | tail -n 29 >> $RES_REPORT

