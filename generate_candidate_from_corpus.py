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
vocab_file = sys.argv[4]
out_file = sys.argv[5]

term_map_dict = cooc.create_cooc(term_file, term_type, corpus_path)    
term_list =cooc.load_terms_to_list(term_file,term_type)
vocab_list=cooc.load_vocab_to_list(vocab_file)
cooc.calculate_candidate_list_write_to_file(term_list,vocab_list,term_map_dict,out_file)