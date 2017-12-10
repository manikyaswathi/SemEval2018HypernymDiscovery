#!/bin/bash

# AUTHOR: MANIKYA SWATHI VALLABHAJOSYULA
# PURPOSE: TO GENERATE STAGE 1 MODEL 2 RESULTS
# ---------------------------------------------------------
# REQUIREMENTS: Needs two command line parameters
# The below command is used to run this program
# ./prepareNew.sh Input.data.txt Filename.output.txt


# if inssuficient parameters, the program quits.
if [[ "$#" -ne 2 ]]; then
    echo "Illegal number of parameters. The script should be run as scriptfile.sh Input.Data.txt Output.Data.txt"
else
    # CLEAN UP FOLDER BEFOE STARTUP
    chmod -R 755 *
    for count in `seq 1 26`
    do
	if [ -d "$count" ]; then
	    rm -R $count
	fi
    done
    if [ -f "train*" ]; then
	rm traina*
    fi
    # Clean Up complete

    FILE="$1"                       # INPUT FILE with INPUT TERMS - TRAINING.DATA.TXT or TRIAL.DATA.TXT
    OFILE="$2"                      # RESULT FILE FOR Stage2 Model 2 : Stage2_Model1_train.txt

    # Getting the Sample size from input file - creats subfolders to execute Model1 program parallely.
    # Each paraller Model1 run gets results for 100 hyponyms max
    # maximum capcity of the sample size is 2600
    # All the programs and depedencies needed to run each instance are copied into its respective folder
    SAMPLESIZE=`cat $FILE | wc -l`
    echo "Size of target words : $SAMPLESIZE"  >> Model1.LOG
    DIV=100
    QUO=$((SAMPLESIZE / DIV))
    LEFT=$((SAMPLESIZE % DIV))
    if [[ "$LEFT" -ne 0 ]]; then
	NO_OF_FOLDERS=$((QUO+1))
    else
	NO_OF_FOLDERS=$QUO
    fi
    echo "NO OF FOLDERS Created for MODEL 1 : $NO_OF_FOLDERS" >> Model1.LOG
    # splitting the input file
    split -l 100 $FILE train

    # max 2600 = 100* 26 files
    filename=(trainaa trainab trainac trainad trainae trainaf trainag trainah trainai trainaj trainak trainal trainam trainan trainao trainap trainaq trainar trainas trainat trainau trainav trainaw trainax trainay trainaz)
    # Copying the following:
    # 1. Make a temp folder
    # 2. Copy the stemming module
    # 3. Copy the UMBCCEIS.txt - all the is (a|an|the) hearst pattern Hyponym ; hypernym pairs
    # 4. Copy the candidate Vocabulary file 1A.english.vocabulary.txt
    # 5. Copy the respective split of the input file
    # 6. Copy the main Python Module of Model 1 - Stage2Model1IsA.py
    for count in `seq 1 $NO_OF_FOLDERS`
    do
        echo "Creting folder $count" >> Model1.LOG
        mkdir $count
        cp -R stemming $count/
        cp UMBCCEIS.txt $count/
        cp 1A.english.vocabulary.txt $count/
        location=$count-1
        cp ${filename[$location]} $count/
        cp Stage2Model1IsA.py $count/
    done
fi

chmod -R 777 *
wait

# Namvigating into each temp folder and invoking the execute of Model 1
for count1 in `seq 1 $NO_OF_FOLDERS`
do
    echo "RUNNING script in folder $count1" >> Model1.LOG
    location=$((count1-1))
    #echo "---$location"
    #echo ${filename[$location]}
    python $count1/Stage2Model1IsA.py $count1/${filename[$location]} &
done

# Waiiting for all the runs of Model 1 to complete
wait

# Navigating into each temp folder and merging the results into one output File $OFILE
for count in `seq 1 $NO_OF_FOLDERS`
do
    echo "Copying files from $count folder to result file" >> Model1.LOG
    location=$count-1
    finalF=$count/${filename[$location]}".op.txt"
    sed -n -e '1,100p' $finalF >> $OFILE
done

# Once the main putput file is created, Delete the temp folders.
echo "Deleting the folders and the split files" >> Model1.LOG

for count in `seq 1 $NO_OF_FOLDERS`
do
    rm -R $count
done

# Deleting the temp split.
rm traina*
