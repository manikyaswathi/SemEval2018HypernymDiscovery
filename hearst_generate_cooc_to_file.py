# -*- coding: utf-8 -*-
"""
@Team Babbage : CS 8761 Project
@SemEval-2018 Task 9: Hypernym Discovery
@author: Arshia Zernab Hassan

@File : hearst_generate_cooc_to_file.py

This is a driver file to create an intermidiate dictionary and save it to file.
First a intermidiate dictionary is created using the input terms (read from file) and data corpus.
Then the dictionary is written to an external file.

It calls the necessary functions stated in hearst.py. Plaese refer to hearst.py for detail descriptions.

First command line argument : name of the text file (.txt format) contaning the input terms which should be in the same directory as the source codes
Second  command line argument : directory path of the corpus which should contain the corpus .txt files
Third command line argument : output text file name (.txt format)
"""
import hearst
import sys

term_file = sys.argv[1]
corpus_path = sys.argv[2]
out_file = sys.argv[3] 

hyp_map_dict = hearst.create_term_hyper_freq_map_from_file(term_file,corpus_path)#create dictionary
if bool(hyp_map_dict):
    	success = hearst.write_hyp_dict_to_file(hyp_map_dict, out_file)#write dictionary to file
    	if success==True :
    		print "Map written to " + out_file + "successfully."
    	else :
    		print "Process was unsuccessful."
