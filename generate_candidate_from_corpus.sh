#!/bin/bash

#Created on Mon Oct 09 21:44:40 2017

#@author: Arshia Zernab Hassan

#First command line argument : name of the text file (.txt format) containing the input terms which should be in the same directory as the source codes
#Second  command line argument : type of the term as a string ("concept" or "entity")
#Third  command line argument : directory path of the corpus which should contain the corpus .txt files
#Forth command line argument : name of the text file (.txt format) containing the vocabulary
#Fifth command line argument : output text file name (.txt format)

#Runs - generate_candidate_from_corpus.py

#Sample run command : ./generate_candidate_from_corpus.sh "term.txt" "concept" "test/" "vocab.txt" "out.txt"

term_file=$1
term_type=$2
corpus_path=$3
vocab_file=$4
out_file=$5

python generate_candidate_from_corpus.py $term_file $term_type $corpus_path $vocab_file $out_file
