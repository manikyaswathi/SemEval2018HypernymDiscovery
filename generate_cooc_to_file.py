# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 21:44:40 2017

@author: Arshia Zernab Hassan
"""

import cooc
import sys

term_file = sys.argv[1]
term_type = sys.argv[2]
corpus_path = sys.argv[3]
out_file = sys.argv[4] 

term_map_dict = cooc.create_cooc(term_file, term_type, corpus_path)
success = cooc.write_cooc_to_file(term_map_dict, out_file)
if success==True :
    print "Map written to " + out_file + "successfully."
else :
    print "Process was unsuccessful."
