# -*- coding: utf-8 -*-
"""
@Team Babbage : CS 8761 Project
@SemEval-2018 Task 9: Hypernym Discovery
@author: Arshia Zernab Hassan

@file : hearst_generate_candidate_load_map.py

This is a driver file to generate output using from loaded dictionary.
The dictionary is pre created possibly using  hearst_generate_cooc_to_file.py
First the intermidiate dictionary is loaded from a file.
Input terms and vocabulary words are also loaded from file to separate lists.
The output is generated using the dictionary, input term list, vocabulary list and written to an external file.

It calls the necessary functions stated in hearst.py. Plaese refer to hearst.py for detail descriptions.

It calls the necessary functions stated in cooc.py. Plaese refer to cooc.py for detail descriptions of the functions.
First command line argument : name of the text file (.txt format) containing the input terms which should be in the same directory as the source codes
Second  command line argument : name of the text file (.txt format) containing the hyponym-hypernym cooc dictionary which should be in the same directory as the source codes
Third command line argument : name of the text file (.txt format) containing the vocabulary which should be in the same directory as the source codes
Forth command line argument : output text file name (.txt format)
"""

import hearst
import sys


term_file = sys.argv[1]
term_map_file = sys.argv[2]
vocab_file = sys.argv[3]
out_file = sys.argv[4]


term_map_dict=hearst.load_hyp_from_file(term_map_file) #load dictionary
if bool(term_map_dict) :    
	term_list =hearst.load_terms_to_list(term_file) #load input terms
	vocab_list=hearst.load_vocab_to_list(vocab_file) #load vocabulary
	hearst.calculate_candidate_list_write_to_file(term_list,vocab_list,term_map_dict,out_file) #generate and write output to file
