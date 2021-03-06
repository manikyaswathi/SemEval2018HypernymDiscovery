# -*- coding: utf-8 -*-
"""
@Team Babbage : CS 8761 Project
@SemEval-2018 Task 9: Hypernym Discovery
@author: Arshia Zernab Hassan

@file : generate_candidate_from_corpus.py

This is a driver file to generate output using corpus data. 

First a intermidiate dictionary is created using the input terms (read from file) and data corpus.
Input terms and vocabulary words are loaded from file to separate lists.
The output is generated using the dictionary, input term list, vocabulary list and written to an external file.

It calls the necessary functions stated in cooc.py. Plaese refer to cooc.py for detail descriptions.

First command line argument : name of the text file (.txt format) containing the input terms which should be in the same directory as the source codes
Second  command line argument : directory path of the corpus which should contain the corpus .txt files
Third command line argument : name of the text file (.txt format) containing the vocabulary
Forth command line argument : output text file name (.txt format)
"""

import cooc
import sys

term_file = sys.argv[1]
corpus_path = sys.argv[2]
vocab_file = sys.argv[3]
out_file = sys.argv[4]

term_map_dict = cooc.create_cooc(term_file, corpus_path)  #create dictionary    
term_list =cooc.load_terms_to_list(term_file) #load input terms
vocab_list=cooc.load_vocab_to_list(vocab_file) #load vocabulary
cooc.calculate_candidate_list_write_to_file(term_list,vocab_list,term_map_dict,out_file) #generate and write output to file