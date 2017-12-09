# -*- coding: utf-8 -*-
"""
@Team Babbage : CS 8761 Project
@SemEval-2018 Task 9: Hypernym Discovery
@author: Arshia Zernab Hassan

@File_name : hearst.py

@File description:
Set of functions to generate output hypernym candidate lists given a set of input terms, data corpus and vocabulary list.
This module works on data corpus normalized using the Hearst algorithm.
 The output is a candidate hypernym list produced taking into account their co-occurance frequency with the input word in the Hearst-normalzed data set.

@Data requirements :

1. Data corpus provided should be normalized by the Hearst algorithm and should be in a special format for this module to work. 
#format of each line in file :
    hyponym	: hypernym_1 , hypernym_2

2. Input files words are normalized to contain only lowercase letters and space between a compound word is replaced by _.
#format of each line in file : Tab <\t> separated - 
	input_term <\t> input_type
We do not take into account the input type for this algorithm and discard it.

3. vocabulary files words are normalized to contain only lowercase letters and space between a compound word is replaced by _.

4. Output file produced contains tab separated list of candidates. 
The line number is alligned with that of the input file (following the format provided in the SemEval task description). 
#format of each line in file: Tab <\t> separated - 
candidate_1<\t>candidate_2

@General Assumptions :

We refer to "dictionary" as a mapping of hyponyps to hypernyms, as opposed to word meanings.
We refer to "term" as input hyponyms.

Agian the module is tuned to specifically work on the Data requirements stated above. It will not work if data is not normalized.

First our intuition was to create a dictionary that would map each hyponym with their hypernyms and respective frequencies
 of the hypernyms co-occuring with that hyponym.The function (create_hypo_hyper_freq_map_from_file) was written with that view in mind.
 But the proccessing time was 2 minutes per file on average. For 408 files it would take a lot of time. So we did not use this function
 to create a all encompassing dictionary. The advantage of that dictionary if created once from the data corpus, it can be reused for 
 any number of new test input data.

We instead created a dictionary based on the input data. Function (create_term_hyper_freq_map_from_file) thus creates a dictionary that only contains 
the set of input terms as indices and maps to only their candidate hypernyms. So this is more of an intermidiate data structure strictly build for the input data.
For 50 (trial data) and 1000(training data) input terms and 408 data files in corpus, this implementation takes about an hour creating internal dictionary from 
corpus and producing output.  Although we have added provision to write the intermiditate dictionary to file and load data from it to create outputs, 
this will not work for hyponyms not in the input list. Loading dictionary from file is for testing purposes for now, 
but will be useful when we will be using pre-created large dictionaries that covers more input terms.

The function(sort_candidates) sorts the candidate hypernyms for a term in descending order of their frequency.
 We have added a threshold value of frequency, so if a hypernym does not occur more than the threshold value it will not be considered. 
 Currently threshold is set to 0 as the list of candidates are not so large for the Hearst dataset and it is not affecting the computation time.

For generating final outputs in function (calculate_candidate_list_write_to_file), we ended up NOT using the vocabulary list provided
 to check if the candidate hypernyms are from the vocabulary. We need to post-process the generated candidate hypernyms 
 in order to compare them with words in the vocabulary applying complete string matching. From a human perspective, 
 some generated hypernyms do not match any word from vocabulary but are correct ones. Post-processing () would improve this situation.

@Function List :
create_hypo_hyper_freq_map_from_file(corpus_path)
create_term_hyper_freq_map_from_file(term_file,corpus_path)
write_hyp_dict_to_file(hyp_map_dict, filename)
load_hyp_from_file(filename)
load_terms_to_list(file_name)
load_vocab_to_list(file_name)
sort_candidates(hyp_list, thresh)
calculate_candidate_list_write_to_file(term_list,vocab_list,hyp_map_dict,filename)
"""

from collections import defaultdict
import os
import re

"""
#Function name : create_hypo_hyper_freq_map_from_file
#Author : Arshia Zernab Hassan
#This function creates dictionary for all the hyponyms in the corpus created using hearst algorithm
#Function description : 
 Creates A dictionary of hyponyms mapped to dictionaries that maps hypernyms to their frequencies
-reads from file a list of hyponyms with a list of hypernyms separated by " : "
-for each .txt file in the corpus directory add hypernyms 
that occur in the same line with the hyponym and also their frequencies
to the dictionary mapped by the hyponym as a key. 
##the corpus is produced using Hearst Algorithm
#line format in file :
    hyponym : hypernym_1 , hypernym_2
#Input Parameters : 
corpus_path (path of the directory containing 
all the training data files in .txt format)
#Output : 
A dictionary of terms mapped to dictionaries that maps words to their frequencies 
#pre-condition : 
    1.corpus_path is valid
    2. corpus contains
""" 
def create_hypo_hyper_freq_map_from_file(corpus_path) :
    hypo_hyper_dict = defaultdict(dict)#dictionary mapping
    try:
        for filename in os.listdir(corpus_path) :#for each file in corpus directory
            if filename.endswith(".txt"): #if it is a text file
                file_ptr = open(os.path.join(corpus_path.strip()+filename),'r') #open file
                for line in file_ptr :
                    if bool(re.search(':',line)) :                       
                        hyper, value = re.split(" : ",line,1) #
                        if value != '\n' : #value has one or more co-occured words with a term
                           value.strip(' , ')  #strip the ending ', ' from value                    
                           value_list = re.split(" , ",value)#tokenize word-frequency pair using " , "
                           #value_list.remove('\n')#remove newline character from word-frequency string list
                           #hypo_set = set(value_list)
                           for hypo in value_list:
                               hypo = hypo.strip()
                               if hypo in hypo_hyper_dict.iterkeys() :
                                   if hyper in hypo_hyper_dict[hypo].iterkeys():
                                       hypo_hyper_dict[hypo][hyper]+=1
                                   else : 
                                       hypo_hyper_dict[hypo][hyper] = 1
                               else :
                                   hypo_hyper_dict[hypo][hyper] = 1 
                file_ptr.close()
        return hypo_hyper_dict
    except IOError:
        print "Could not open file!"

"""
#Function name : load_terms_to_dict
#Author : Arshia Zernab Hassan
#Function description : 
-reads from file the list of terms 
-depending on the input string extracts the concept or the entities
-creates dictionary mapping term to an empty dictionary
#Input Parameters : 
filename (name of the file that contains input terms)
id_string (type of term (entity or concept))
#Output : 
A dictionary of terms mapped to empty dictionaries that would map words to their frequencies
#pre-condition : 
    1.filename is valid
    2.file contains tab delimited terms and type on each line(i.e. )
"""
def load_terms_to_dict(file_name) :

    try:    
        term_map_dict = defaultdict(dict)    
        file_ptr = open(file_name,'r') #open file
        for line in file_ptr :
            term, identity = line.split('\t',1)
            term_map_dict[term] = defaultdict(int)
        file_ptr.close() #close file     
        return term_map_dict
    except IOError:
        print "Could not open file!"

"""
#Function name : create_term_hyper_freq_map_from_file
#Author : Arshia Zernab Hassan
#This function creates dictionary only for the input terms
#Function description : 
 Creates A dictionary of input terms mapped to dictionaries that maps hypernyms to their frequencies
-reads from file a list of input terms and create a dictionary mapping terms to empty dictionaries
-reads from file a list of hyponyms with a list of hypernyms separated by " : "
-for each .txt file in the corpus directory add hypernyms 
that occur in the same line with the hyponym (input term) and also their frequencies
to the dictionary mapped by the hyponym as a key. 
##the corpus is produced using Hearst Algorithm
#line format in file :
    hyponym : hypernym_1 , hypernym_2    
#Input Parameters : 
term_file (name of the file that contains input terms)
corpus_path (path of the directory containing 
all the training data files in .txt format)
#Output : 
A dictionary of terms mapped to dictionaries that maps words to their frequencies 
#pre-condition : 
    1.corpus_path is valid
    2.term filename is valid
    3.file contains tab delimited terms and type on each line(i.e. )
"""		
def create_term_hyper_freq_map_from_file(term_file,corpus_path) :
    try:
        term_map_dict = load_terms_to_dict(term_file)
        key_list = term_map_dict.keys()
        if bool(term_map_dict) :
            for filename in os.listdir(corpus_path) :#for each file in corpus directory 
                if filename.endswith(".txt"): #if it is a text file
                    file_ptr = open(os.path.join(corpus_path.strip()+filename),'r') #open file
                    for line in file_ptr :
                        if bool(re.search(' : ',line)) :                       
                            hyper, value = re.split(" : ",line,1) #
                            if value != '\n' : #value has one or more co-occured words with a term
                               value.strip(' , ')  #strip the ending ', ' from value                    
                               value_list = re.split(" , ",value)#tokenize word-frequency pair using " , "
                               for hypo in value_list:
                                   hypo = hypo.strip()
                                   for term in key_list :
                                       if (term in hypo):
                                           term_map_dict[term][hyper]+=1                                       
                    file_ptr.close()
        return term_map_dict
    except IOError:
        print "Could not open file!"
"""
#Function name : write_hyp_dict_to_file
#Author : Arshia Zernab Hassan
#Function description : Writes a co-occurance dictionary to the input file
#format of each line in file:
term_name : word1 freq1 , word2 freq2 ,
#Input Parameters :
hyp_map_dict (A dictionary of hyponyms mapped to dictionaries that maps hypernyms to their frequencies)
filename (name of the file to contain co-occurance dictionary)
#Output : 
N/A
#pre-condition : 
    1.filename does not exist already to avoid overwriting
    2. term_map_dict is a valid dictionary of terms mapped to dictionaries that maps words to their frequencies
"""         
def write_hyp_dict_to_file(hyp_map_dict, filename):
    try:
        file_ptr_out = open(filename,'w')       
        for key,value in hyp_map_dict.iteritems():
            dict_string = key + " : " 
            for key2, value2 in value.iteritems() :        
                dict_string = dict_string + key2 + "\t" + str(value2) + " , "  
            dict_string = dict_string + "\n"    
            file_ptr_out.write(dict_string)
        file_ptr_out.close()
        return True
    except IOError:
        print "Could not open file!"
        return False
        
"""
#Function name : load_hyp_from_file
#Author : Arshia Zernab Hassan
#Function description : Loads a co-occurance dictionary from the input file 
#format of each line in file:
term_name : word1 freq1 , word2 freq2 ,
#Input Parameters : 
filename (name of the file that contains co-occurance dictionary)
#Output : 
A dictionary of hyponyms mapped to dictionaries that maps hypernyms to their frequencies
#pre-condition : 
    1.filename is valid
    2.file contains co-occurance dictionary - hyponyms mapped to dictionaries that maps hypernyms to their frequencies
"""         
def load_hyp_from_file(filename) :
    hyp_map_dict = defaultdict(dict)
    try:
        file_ptr = open(filename,'r')
        for line in file_ptr :
            if bool(re.search(':',line)) : 
                key, value = re.split(" : ",line,1) #key is term, value is comma separated word-frequency pair
                hyp_map_dict[key] = defaultdict(int)
                if value != '\n' : 
                   value.strip(' , ')  #strip the ending ', ' from value                    
                   value_list = re.split(" , ",value)#tokenize word-frequency pair using " , "
                   #value_list.remove('\n')#remove newline character from word-frequency string list
                   for element in value_list : #for each word-frequency pair string
                       element = element.strip()
                       if bool(re.search('\t',element)) :
                           key2, value2 = element.split('\t',1) #tokenize using whitespace character
                           value2 = int(value2.strip())#remove newline character
                           hyp_map_dict[key][key2]=value2  #add frequency to dictionary mapped by term and word 
        file_ptr.close()
        return hyp_map_dict
    except IOError:
        print "Could not open file!"

"""
#Function name : load_terms_to_list
#Author : Arshia Zernab Hassan
#Function description : 
-reads from file the list of terms to a list
#Input Parameters : 
filename (name of the file that contains input terms)
#Output : 
A list of terms 
#pre-condition : 
    1.filename is valid
    2.file contains tab delimited terms and type on each line(i.e. )
""" 
def load_terms_to_list(file_name) :
    try:    
        term_list = list()    
        file_ptr = open(file_name,'r') #open file
        for line in file_ptr :
            term, identity = line.split('\t',1)
            term_list.append(term)
        file_ptr.close() #close file 
        return term_list
    except IOError:
        print "Could not open file!"

"""
#Function name : load_vocab_to_list
#Author : Arshia Zernab Hassan
#Function description : 
-reads from file the list of vocabulary to a list
#Input Parameters : 
filename (name of the file that contains vocabulary of hypernyms)
#Output : 
A list of vocabulary 
#pre-condition : 
    1.filename is valid
    2.file contains vocabulary word at each line
""" 
def load_vocab_to_list(file_name) :    
    try:
        vocab_list = list()
        file_ptr = open(file_name,'r') #open file
        for line in file_ptr :
            vocab = line.strip()
            vocab_list.append(vocab)
        file_ptr.close() #close file         
        return vocab_list
    except IOError:
        print "Could not open file!" 

"""
#Function name : sort_candidates
#Author : Arshia Zernab Hassan
#Function description : Given a dictionary of words(key)
 mapping to frequency(value) output a list of the most
 frequent words. 
 Threshold is set to shorten list depending on frequency
so that less frequent (i.e. frequency of 1) words are not
considered in determining the candidates, thus reducing 
time of computation.
#Input Parameters : 
cooc_list (A dictionary mapping words to frequency)
thresh (threshold depending on frequency )
#Output : 
A sorted list of words over the frequency
#pre-condition : hyp_list is not empty
"""        
def sort_candidates(hyp_list, thresh) :
    sorted_candidates = list()
    for word in sorted(hyp_list, key=hyp_list.get, reverse=True):
        if hyp_list[word] > thresh :
            sorted_candidates.append(word)
    return sorted_candidates
"""
#Function name : calculate_candidate_list_write_to_file
#Author : Arshia Zernab Hassan
#Function description : writes to file 
-in each line list of hypernym candidates separated by tab
#format of each line in file: Tab separated - 
candidate_1<\t>candidate_2
#Input Parameters :
term_list (A list of input terms )
vocab_list(A list of vocabulary )
term_map_dict (A dictionary of terms mapped to dictionaries that maps words to their frequencies)
filename (name of the file to write list of hypernym candidates )
#Output : 
N/A
#pre-condition : 
    1.filename does not exist already to avoid overwriting
    2. term_map_dict is a valid dictionary of terms mapped to dictionaries that maps words to their frequencies
    3. term list contains the terms used as key in the term_map_dict
    4. vocab list contains the hypernym vocabulary
"""           
def calculate_candidate_list_write_to_file(term_list,vocab_list,hyp_map_dict,filename) :
    try:
        file_ptr_out = open(filename,'w')
        if bool(term_list) :
			for term in term_list :
				candidate_string = ""
				if term in hyp_map_dict.iterkeys() :
					candidate_list = sort_candidates(hyp_map_dict[term],0)
					for hyp in candidate_list :
						#if hyp in vocab_list :
						candidate_string = candidate_string + hyp + "\t"
					file_ptr_out.write(candidate_string + '\n')
        file_ptr_out.close()
        return True
    except IOError:
        print "Could not open file!" 
        return False
 
 