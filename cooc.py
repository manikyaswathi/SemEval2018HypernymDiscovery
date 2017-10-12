# -*- coding: utf-8 -*-
"""
@Team Babbage : CS 8761 Project
@SemEval-2018 Task 9: Hypernym Discovery
@author: Arshia Zernab Hassan

@File_name : cooc.py

@File description:
Set of functions to generate output hypernym candidate lists given a set of input terms, data corpus and vocabulary list.
 The output is a candidate hypernym list produced taking into account their co-occurance frequency with the input word in the normalzed data set.

@Data requirements :

1. Data corpus provided should be normalized for this module to perform better. The details of the normalization process provided with that module.

2. Input files words are normalized to contain only lowercase letters and space between a compound word is replaced by _.
#format of each line in file : Tab <\t> separated - 
	input_term <\t> input_type
We do not take into account the input type for this algorithm and discard it.

3. Vocabulary files words are normalized to contain only lowercase letters and space between a compound word is replaced by _.

4. Output file produced contains tab separated list of candidates. The line number is alligned with that of the input file (following the format provided in the SemEval task description). 
#format of each line in file: Tab <\t> separated - 
candidate_1<\t>candidate_2

@General Assumptions :

We refer to "dictionary" as a mapping of hyponyps to hypernyms, as opposed to word meanings.
We refer to "term" as input hyponyms.

Agian the module is tuned to specifically work on the Data requirements stated above. It will not work perform accordingly if data is not normalized.

Our algorithm traverse the whole data set line by line to produce the intermidiate dictionary. 
For each line we do the following. We search if their is a input term in the line and add all the words (and update the frequencies)
 in that line to the word-frequncy list mapped by the input term.If the input term is occuring twice in the line, we update it twice. 
 After the dictionary is created, we sort each co-occurance list associated with the input term in descending order of the frequency.
The candidate hypernym list is the sorted list of the co-occured words based on frequency. We only take candidates that are also in the vocabulary.

First our intuition was to create a dictionary that would map every word in data corpus with the words co-occuring with them in the same lines.
But the proccessing time was considerably large, given 408 files. So we did not create a all encompassing dictionary. 
The advantage of that dictionary if created once from the data corpus, it can be reused for any number of new test input data.

We instead created a dictionary based on the input data. Function (create_cooc) thus creates a dictionary that only contains 
the set of input terms as indices and maps to only their candidate hypernyms. So this is more of an intermidiate data structure
 strictly build for the input data.For 50 (trial data) input terms and 408 data files in corpus, this implementation takes more 
 that two hours creating internal dictionary from corpus and producing output.  Although we have added provision to write the 
 intermiditate dictionary to file and load data from it to create outputs, this will not work for hyponyms not in the input list.
 Loading dictionary from file is for testing purposes for now, but will be useful when we will be using pre-created large dictionaries
 that covers more input terms.

The function(sort_candidates) sorts the candidate hypernyms for a term in descending order of their frequency.
 We have added a threshold value of frequency, so if a hypernym does not occur more than the threshold value it will not be considered. 
 Currently threshold is set to 5 as the to not consider the words occuring fewer times to reduce run time of the module.
 
 We wanted to make use of frequency of frequencies to dynamically set the threshold, maybe different values for each input term.
Function (write_freq_of_freq_to_file) was created to achive that. But we decided not to incprporate for now. 


@function list
sorted_cooc(cooc_list, thresh)
freq_of_freq(cooc_list)
load_cooc_from_file(filename)
write_cooc_to_file(term_map_dict, filename)
load_terms_to_dict(file_name)
load_terms_to_list(file_name)
load_vocab_to_list(file_name)
create_cooc(term_file, term_type, corpus_path) 
write_freq_of_freq_to_file(term_list, term_map_dict, file_name)
calculate_candidate_list_write_to_file(term_list,vocab_list,term_map_dict,filename)

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
			if bool(re.search(':',line)) : 
				key, value = re.split(" : ",line) #key is term, value is comma separated co-occured word-frequency pair
				term_map_dict[key] = defaultdict(int)
				if value != '\n' : #value has one or more co-occured words with a term
				   value.strip(' , ')  #strip the ending ' , ' from value                    
				   value_list = re.split(" , ",value)#tokenize word-frequency pair using " , "
				   #value_list.remove('\n')#remove newline character from word-frequency string list
				   for element in value_list : #for each word-frequency pair string
						element = element.strip()
						if bool(re.search('\t',element)) :
						   
						   key2, value2 = element.split('\t',1) #tokenize using whitespace character
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
                dict_string = dict_string + key2 + "\t" + str(value2) + " , " #add word frequency pair separated by white space 
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
corpus_path (path of the directory containing 
all the training data files in .txt format)
#Output : 
A dictionary of terms mapped to dictionaries that maps words to their frequencies 
#pre-condition : 
    1.corpus_path is valid
    2.term filename is valid
    3.file contains tab delimited terms and type on each line(i.e. )
"""     
def create_cooc(term_file, corpus_path) :    
    try:
        concept_map_dict = load_terms_to_dict(term_file)
        if bool(concept_map_dict) :
            keys = concept_map_dict.keys() #loads input terms to list   
            for filename in os.listdir(corpus_path) :#for each file in corpus directory
                if filename.endswith(".txt"): #if it is a text file
                   file_ptr = open(os.path.join(corpus_path.strip()+filename),'r') #open file
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
    except IOError:
        print "Could not open file!" 

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
def calculate_candidate_list_write_to_file(term_list,vocab_list,term_map_dict,filename) :
    try:
        file_ptr_out = open(filename,'w') 
        for term in term_list :
            candidate_string = ""
            candidate_list = sorted_cooc(term_map_dict[term],5)
            for hyp in candidate_list :
                if hyp in vocab_list :
                    candidate_string = candidate_string + hyp + "\t"
            file_ptr_out.write(candidate_string + '\n')
        file_ptr_out.close()
        return True
    except IOError:
        print "Could not open file!" 
        return False

           
  