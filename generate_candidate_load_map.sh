#!/bin/bash

#Created on Mon Oct 09 21:44:40 2017

#@author: Arshia Zernab Hassan

#First command line argument : name of the text file (.txt format) containing the input terms which should be in the same directory as the source codes
#Second  command line argument : type of the term as a string ("concept" or "entity")
#Third  command line argument : name of the text file (.txt format) containing the cooc dictionary
#Forth command line argument : name of the text file (.txt format) containing the vocabulary
#Fifth command line argument : output text file name (.txt format)

#Runs - generate_candidate_load_map.py

#Sample run command : ./generate_candidate_load_map.sh "term.txt" "concept" "map.txt" "vocab.txt" "out.txt"

term_file=$1
term_type=$2
term_map_file=$3
vocab_file=$4
out_file=$5

python generate_candidate_load_map.py $term_file $term_type $term_map_file $vocab_file $out_file
