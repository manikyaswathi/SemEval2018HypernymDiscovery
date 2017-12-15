#!/bin/bash

#STAGE1_NORM=1A.english.output.train.norm.txt
#STAGE1_HEARST=1A.english.output.train.hearst.txt
STAGE1_NORM=${2}
STAGE1_HEARST=${3}


#MODEL1=1A.english.Model1.training.op.txt
#PHI1=phi01.txt
#PHI2=phi02.txt
MODEL1=${4}
PHI1=${5}
PHI2=${6}

#FOLDER=TRAIN|TRAINING
FOLDER=${1}
						   		    
STAGE1=Stage1_norm_hearst.txt
PHI=Stage2_PHI_01_02.txt
STAGE1_PHI=Stage1_Stage2_PHIModule.txt
FINALRES=Stage2_Model1_Stage1_Stage2_PHIModule.txt
FINALRESCON=RES.CON.TXT
FINALRESENT=RES.ENT.TXT

GOLD=${7}

RESLOG=Evaluation_Report.LOG

GOLDCON=input.con.txt
GOLDENT=input.ent.txt

DATA=${8}

if [ -f "$RESLOG" ]; then
    rm $RESLOG
fi

if [ -d "$FOLDER" ]; then
    rm -R $FOLDER
    mkdir $FOLDER
else
    mkdir $FOLDER
fi


if [ -d "$FOLDER" ]; then
    cp MergeResults.sh $FOLDER/
    cp task9-scorer.py $FOLDER/
    cp mergeTwoResults.py $FOLDER/
    cp SeparateCEOp.py $FOLDER/
    cp $STAGE1_NORM $FOLDER/
    cp $STAGE1_HEARST $FOLDER/
    cp $MODEL1 $FOLDER/
    cp $PHI1 $FOLDER/
    cp $PHI2 $FOLDER/
    cp $GOLD $FOLDER/
    cp $DATA $FOLDER/
    cd $FOLDER
    echo "ignore remove errors"
    rm $STAGE1 $PHI $STAGE1_PHI $FINALRES $FINALRESCON $FINALRESENT $GOLDCON $GOLDENT $RESLOG
    touch $STAGE1 $PHI $STAGE1_PHI $FINALRES $FINALRESCON $FINALRESENT $GOLDCON $GOLDENT $RESLOG
    ./MergeResults.sh $STAGE1_NORM $STAGE1_HEARST $MODEL1 $PHI1 $PHI2 $STAGE1 $PHI $STAGE1_PHI $FINALRES $FINALRESCON $FINALRESENT $GOLD $GOLDCON $GOLDENT $DATA $RESLOG &
    cd ..
    wait
else
    echo "FAILED with runMergeEval.sh" > $RESLOG
fi
