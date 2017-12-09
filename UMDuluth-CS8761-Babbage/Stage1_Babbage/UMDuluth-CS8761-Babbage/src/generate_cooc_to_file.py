# -*- coding: utf-8 -*-
"""
@Team Babbage : CS 8761 Project
@SemEval-2018 Task 9: Hypernym Discovery
@author: Arshia Zernab Hassan

@File : generate_cooc_to_file.py

This is a driver file to create an intermidiate dictionary and save it to file.
First a intermidiate dictionary is created using the input terms (read from file) and data corpus.
Then the dictionary is written to an external file.

It calls the necessary functions stated in cooc.py. Plaese refer to cooc.py for detail descriptions.

First command line argument : name of the text file (.txt format) contaning the input terms which should be in the same directory as the source codes
Second  command line argument : directory path of the corpus which should contain the corpus .txt files
Third command line argument : output text file name (.txt format)
"""
import cooc
import sys

term_file = sys.argv[1]
corpus_path = sys.argv[2]
out_file = sys.argv[3] 

term_map_dict = cooc.create_cooc(term_file, corpus_path)#create dictionary
if bool(term_map_dict) :
	success = cooc.write_cooc_to_file(term_map_dict, out_file)#write dictionary to file
	if success==True :
		print "Map written to " + out_file + "successfully."
	else :
		print "Process was unsuccessful."
