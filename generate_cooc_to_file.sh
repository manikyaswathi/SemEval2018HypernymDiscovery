#!/bin/bash

#Created on Mon Oct 09 21:44:40 2017

#@author: Arshia Zernab Hassan

#First command line argument : name of the text file (.txt format) containing the input terms which should be in the same directory as the source codes
#Second  command line argument : type of the term as a string ("concept" or "entity")
#Third  command line argument : directory path of the corpus which should contain the corpus .txt files
#Forth command line argument : output text file name (.txt format)

#Runs - generate_cooc_to_file.py

#Sample run command : ./generate_cooc_to_file.sh "term.txt" "concept" "test/" "map.txt"

term_file=$1
term_type=$2
corpus_path=$3
out_file=$4

python generate_cooc_to_file.py $term_file $term_type $corpus_path $out_file
