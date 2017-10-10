# -*- coding: utf-8 -*-
"""
Created on Thu Oct 05 00:09:43 2017

@author: Arshia
"""

from collections import defaultdict
import os
import re
#import sys

"""
#Function name : sorted_cooc
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
#pre-condition : cooc_list is not empty
"""
def sorted_cooc(cooc_list, thresh) :
    sorted_candidates = list()
    for word in sorted(cooc_list, key=cooc_list.get, reverse=True):
        if cooc_list[word] > thresh :
            sorted_candidates.append(word)
    return sorted_candidates

"""
#Function name : freq_of_freq
#Author : Arshia Zernab Hassan
#Function description : Given a dictionary of words(key)
 mapping to frequency(value) output a dictionary of frequency
 of frequencies. 
#Input Parameters : 
cooc_list (A dictionary mapping words to frequency)
#Output : 
A dictionary of frequency of frequency
#pre-condition : cooc_list is not empty
"""    
def freq_of_freq(cooc_list) :
     counter = defaultdict( int )
     for key,value in cooc_list.iteritems():
         counter[value]+=1
     return counter

"""
#Function name : load_cooc_from_file
#Author : Arshia Zernab Hassan
#Function description : Loads a co-occurance dictionary from the input file 
#format of each line in file:
term_name : word1 freq1 , word2 freq2 ,
#Input Parameters : 
filename (name of the file that contains co-occurance dictionary)
#Output : 
A dictionary of terms mapped to dictionaries that maps words to their frequencies
#pre-condition : 
    1.filename is valid
    2.file contains co-occurance dictionary mapping terms 
    to dictionary of word mapped to frequency 
""" 
def load_cooc_from_file(filename) :
    term_map_dict = defaultdict(dict)#dictionary mapping terms to dictionary of words and frequencies
    try:
        file_ptr = open(filename,'r')
        for line in file_ptr :
            key, value = re.split(" : ",line) #key is term, value is comma separated co-occured word-frequency pair
            term_map_dict[key] = defaultdict(int)
            if value != '\n' : #value has one or more co-occured words with a term
               value.strip(', ')  #strip the ending ', ' from value                    
               value_list = re.split(" , ",value)#tokenize word-frequency pair using " , "
               value_list.remove('\n')#remove newline character from word-frequency string list
               for element in value_list : #for each word-frequency pair string
                   key2, value2 = re.split("\s",element) #tokenize using whitespace character
                   value2 = int(value2.strip())#remove newline character
                   term_map_dict[key][key2]=value2  #add frequency to dictionary mapped by term and word 
        file_ptr.close()
        return term_map_dict
    except IOError:
        print "Could not open file!"      
        
"""
#Function name : write_cooc_to_file
#Author : Arshia Zernab Hassan
#Function description : Writes a co-occurance dictionary to the input file
#format of each line in file:
term_name : word1 freq1 , word2 freq2 ,
#Input Parameters :
term_map_dict (A dictionary of terms mapped to dictionaries that maps words to their frequencies)
filename (name of the file to contain co-occurance dictionary)
#Output : 
N/A
#pre-condition : 
    1.filename does not exist already to avoid overwriting
    2. term_map_dict is a valid dictionary of terms mapped to dictionaries that maps words to their frequencies
"""    
def write_cooc_to_file(term_map_dict, filename):
    try:
        file_ptr_out = open(filename,'w')       
        for key,value in term_map_dict.iteritems():
            dict_string = key + " : " #add term and separator " : " (term and co-occurance list with " : ")
            for key2, value2 in value.iteritems() :        
                dict_string = dict_string + key2 + " " + str(value2) + " , " #add word frequency pair separated by white space 
            dict_string = dict_string + "\n"    
            file_ptr_out.write(dict_string)
        file_ptr_out.close()
        return True
    except IOError:
        print "Could not open file!"
        return False
        
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
def load_terms_to_dict(file_name, id_string) :

    try:    
        term_map_dict = defaultdict(dict)    
        file_ptr = open(file_name,'r') #open file
        for line in file_ptr :
            term, identity = line.split('\t',1)
            identity = identity.strip()
            if identity==id_string :
                term_map_dict[term] = defaultdict(int)
        file_ptr.close() #close file     
        return term_map_dict
    except IOError:
        print "Could not open file!"
        
"""
#Function name : load_terms_to_list
#Author : Arshia Zernab Hassan
#Function description : 
-reads from file the list of terms to a list
#Input Parameters : 
filename (name of the file that contains input terms)
id_string (type of term (entity or concept))
#Output : 
A list of terms 
#pre-condition : 
    1.filename is valid
    2.file contains tab delimited terms and type on each line(i.e. )
"""    
def load_terms_to_list(file_name, id_string) :
    try:    
        term_list = list()    
        file_ptr = open(file_name,'r') #open file
        for line in file_ptr :
            term, identity = line.split('\t',1)
            identity = identity.strip()
            if identity==id_string :
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
#Function name : create_cooc
#Author : Arshia Zernab Hassan
#Function description : 
 Creates A dictionary of terms mapped to dictionaries that maps words to their frequencies
-reads from file a list of input terms and create a dictionary mapping terms to empty dictionaries
-for each .txt file in the corpus directory add words 
that occur in the same line with the term and their frequencies
to the dictionary mapped by the term as a key.    
#Input Parameters : 
term_file (name of the file that contains input terms)
term_type (type of term ('entity' or 'concept'))
corpus_path (path of the directory containing 
all the training data files in .txt format)
#Output : 
A dictionary of terms mapped to dictionaries that maps words to their frequencies 
#pre-condition : 
    1.corpus_path is valid
    2.term filename is valid
    3.file contains tab delimited terms and type on each line(i.e. )
"""     
def create_cooc(term_file, term_type, corpus_path) :    
    concept_map_dict = load_terms_to_dict(term_file, term_type)
    keys = concept_map_dict.keys() #loads input terms to list   
    path = corpus_path
    for filename in os.listdir(path) :#for each file in corpus directory
        if filename.endswith(".txt"): #if it is a text file
           file_ptr = open(path.strip()+filename,'r') #open file
           for line in file_ptr : # for each line in file           
               line = line.strip("\n") # delete newline character from line               
               # get the list of input terms that are in the current line
               term_list = list()
               for term in keys : #for all input terms 
                   if term in line : #if input term is a word in the line
                      term_list.append(term) #save term to list
               #update the frequencies of the words in the line 
               #mapped by the terms in the line             
               word_list = line.split()#tokenize and retrieve words from the line
               for word in word_list : #for each word in line
                   for term in term_list : #for each term in line
                       if word is not term :
                           word = word.strip("\s") #strip word of any whitespace character
                           concept_map_dict[term][word]+=1 #update the frequency of the word co-occuring with the term
           file_ptr.close() #close file 
    """empty = ''
    if empty in concept_map_dict.keys() :
        concept_map_dict.pop(empty)"""
    return concept_map_dict

"""
#Function name : write_freq_of_freq_to_file
#Author : Arshia Zernab Hassan
#Function description : writes to file 
a dictionary that
-terms as keys
-maps to a dictionary of sorted (descending order) frequency of frequency (of co-occured words)
#format of each line in file: Tab separated - 
term<\t>frequncy_1:frequency_of_frequency_1<\t>frequncy_2:frequency_of_frequency_2  
#Input Parameters :
term_list (A list of input terms )
term_map_dict (A dictionary of terms mapped to dictionaries that maps words to their frequencies)
filename (name of the file to write dictionary mapping terms with frequency of frequency )
#Output : 
N/A
#pre-condition : 
    1.filename does not exist already to avoid overwriting
    2. term_map_dict is a valid dictionary of terms mapped to dictionaries that maps words to their frequencies
    3. term list contains the terms used as key in the term_map_dict
""" 
def write_freq_of_freq_to_file(term_list, term_map_dict, file_name) :    
    try:
        file_ptr_freq = open(file_name,'w')
        for term in term_list :
            freq_string = term + "\t" #input term with tab as separator
            freq_dict = freq_of_freq(term_map_dict[term])
            for w in sorted(freq_dict.iterkeys(), reverse=True) :
                freq_string = freq_string + str(w) +":"+str(freq_dict[w])+"\t" 
            file_ptr_freq.write(freq_string + '\n')
        file_ptr_freq.close()
    except IOError:
        print "Could not open file!" 

"""
#Function name : calculate_candidate_list_write_to_file
#Author : Arshia Zernab Hassan
#Function description : writes to file 
input terms with list of hypernym candidates separated by tab
#format of each line in file: Tab separated - 
term<\t>:<\t>candidate_1<\t>candidate_2
#Input Parameters :
term_list (A list of input terms )
vocab_list(A list of vocabulary )
term_map_dict (A dictionary of terms mapped to dictionaries that maps words to their frequencies)
filename (name of the file to write dictionary mapping terms with frequency of frequency )
#Output : 
N/A
#pre-condition : 
    1.filename does not exist already to avoid overwriting
    2. term_map_dict is a valid dictionary of terms mapped to dictionaries that maps words to their frequencies
    3. term list contains the terms used as key in the term_map_dict
    4. vocab list contains the hypernym vocabulary
"""         
def calculate_candidate_list_write_to_file(term_list,vocab_list,term_map_dict,filename) :
    try:
        file_ptr_out = open(filename,'w') 
        for term in term_list :
            candidate_string = term + "\t:"
            candidate_list = sorted_cooc(term_map_dict[term],5)
            for hyp in candidate_list :
                if hyp in vocab_list :
                    candidate_string = candidate_string + "\t" + hyp
            file_ptr_out.write(candidate_string + '\n')
        file_ptr_out.close()
        return True
    except IOError:
        print "Could not open file!" 
        return False

           
  