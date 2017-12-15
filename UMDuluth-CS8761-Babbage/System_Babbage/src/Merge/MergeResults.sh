#!/bin/bash

# Author = Manikya Swathi vallabhajosyula

# PURPOSE = Merge results of all modules and give an evaluation score

STAGE1_NORM=${1}     # Stage 1 Norm results
STAGE1_HEARST=${2}   # Stage 1 Hearst results 
MODEL1=${3}          # Stage 2 MODEL 1 results 
PHI1=${4}            # Stage 2 PHI Module 01 results 
PHI2=${5}            # Stage 2 PHI Module 02 results 

STAGE1=${6}          # Stage1 NORM + HEARST results : Stage1_NormHearst
PHI=${7}             # Stage 2 Phi Module - Phi 01+02 : Stage2_PHI_01_02 results
STAGE1_PHI=${8}      # Stage1_NormHearst_Stage2_PHI_01_02 results
FINALRES=${9}        # Stage2_Model1_Stage1_NormHearst_Stage2_PHI_01_02 results
FINALRESCON=${10}    # Final Result Concept
FINALRESENT=${11}    # Final Result Entity

GOLD=${12}           # TRIAL | TRAIN Gold data

RESLOG=${16}         # LOG FILE

GOLDCON=${13}        # Gold - CONCEPT
GOLDENT=${14}        # Gold - ENTITY

DATA=${15}           # The TRAINING | TRIAL input trem file

# merge stage 1 results
python mergeTwoResults.py $STAGE1_NORM $STAGE1_HEARST $STAGE1
# merge Stage 2 phi module results
python mergeTwoResults.py $PHI1 $PHI2 $PHI

wait
# merge Stage 1 reulsts with stage 2 Phi module result
python mergeTwoResults.py $STAGE1 $PHI $STAGE1_PHI

wait
# Final merge - stage 2 model 1 with previous merge
python mergeTwoResults.py $MODEL1 $STAGE1_PHI $FINALRES

wait

echo " 1. RESULTS FOR: STAGE 1 - NORMALISED MODULE " >> $RESLOG
echo "            File : $STAGE1_NORM" >> $RESLOG
echo " ********************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $STAGE1_NORM >> $RESLOG
echo " 2. RESULTS FOR: STAGE 1 - HEARST MODULE " >> $RESLOG
echo "            File : $STAGE1_HEARST">> $RESLOG
echo " ********************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $STAGE1_HEARST >> $RESLOG
echo " 3. RESULTS FOR: STAGE 1 - NORM + HEARST MODULEs " >> $RESLOG
echo "            File : $STAGE1">> $RESLOG 
echo " ********************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $STAGE1 >> $RESLOG
echo " 4. RESULTS FOR: PHI MODULE - PHI1  " >> $RESLOG
echo "            File : $PHI1">> $RESLOG
echo "    most_similar(positive=[WORD, PHI*WORD], negative =[])  " >> $RESLOG
echo " ********************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $PHI1 >> $RESLOG
echo " 5. RESULTS FOR: PHI MODULE - PHI2  " >> $RESLOG
echo "            File : $PHI2">> $RESLOG
echo "    most_similar(positive=[WORD], negative=[PHI*WORD])  " >> $RESLOG
echo " ********************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $PHI2 >> $RESLOG
echo " 6. RESULTS FOR: PHI MODULE - PHI1 + PHI2  " >> $RESLOG
echo "            File : $PHI">> $RESLOG
echo " ********************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $PHI >> $RESLOG
echo " 7. RESULTS FOR: STAGE 1 + PHI MODULE " >> $RESLOG
echo "            File : $STAGE1_PHI">> $RESLOG
echo " ********************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $STAGE1_PHI >> $RESLOG
echo " 8. RESULTS FOR: MODEL1 " >> $RESLOG
echo "            File : $MODEL1">> $RESLOG
echo " ********************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $MODEL1 >> $RESLOG
echo " 9. RESULTS FOR: Module 1 + (STAGE 1 + PHI MODULE) [FINAL] RESULTS " >> $RESLOG
echo "            File : $FINALRES">> $RESLOG
echo " ***************************************************************** " >> $RESLOG
python task9-scorer.py $GOLD $FINALRES >> $RESLOG
echo " SEPARATING [FINAL] RESULTS " >> $RESLOG
python SeparateCEOp.py $DATA $FINALRES $FINALRESCON $FINALRESENT
echo " SEPARATING [GOLD] DATA " >> $RESLOG
python SeparateCEOp.py $DATA $GOLD $GOLDCON $GOLDENT
echo " 10. RESULTS FOR: Module 1 + (STAGE 1 + PHI MODULE) [FINAL] CONCEPT RESULTS " >> $RESLOG
echo "            File : $FINALRESCON">> $RESLOG
echo " ************************************************************************** " >> $RESLOG
python task9-scorer.py $GOLDCON $FINALRESCON >> $RESLOG
echo " 11. RESULTS FOR: Module 1 + (STAGE 1 + PHI MODULE) [FINAL] ENTITY RESULTS " >> $RESLOG
echo "            File : $FINALRESENT">> $RESLOG
echo " ************************************************************************** " >> $RESLOG
python task9-scorer.py $GOLDENT $FINALRESENT >> $RESLOG



