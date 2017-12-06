"""
@Team Babbage : CS 8761 Project
@SemEval-2018 Task 9: Hypernym Discovery
@author: Arshia Zernab Hassan

@File_name : Create_hypo_hyper_list_from_train_data.py

@File description:
Reads hyponym and list of gold hypernyms from two separate files and produce a .csv file where each line is - 
hyponym<\t>hypernym

@Data requirements:
1. "1A.english.training.data.txt"
#format of each line in file : Tab <\t> separated - 
	input_term <\t> input_type
We do not take into account the input type for this algorithm and discard it.

2. Gold file produced contains tab separated list of hypernyms. The line number is alligned with that of the input file.
#format of each line in file: Tab <\t> separated - 
hypernym1<\t>hypernym2<\t>hypernym3...

@Output file:
Output is a tab separated csv file- data_train_gold.csv
The first row is : "hyponym	hypernym"
The following rows are of the form hyponym<\t>hypernym
"""
import csv
from itertools import izip

file_gold = "1A.english.training.gold.txt" #gold data file; format on each line : hypernym1<\t>hypernym2<\t>hypernym3...
file_out = "data_train_gold.csv" #.csv file where output should be written
file_in ="1A.english.training.data.txt" #input term data file; format on each line : hyponym<\t>type

file_ptr_gold = open(file_gold,'r')
file_ptr_in = open(file_in,'r')

with open(file_out, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar='\t')
    writer.writerow(['hyponym','hypernym'])#first line of output file should be "hyponym<\t>hypernym"
    for in_line, gold_line in izip(file_ptr_in,file_ptr_gold):# for each same line from input and gold data
        in_line.strip('\n')
        gold_line.strip('\n')
        hypo, identity = in_line.rsplit('\t',1)
        gold_list = list()
        if '\t' in gold_line :
            gold_list = gold_line.split("\t") #if multiple hypernyms extract the hypernyms to a list
        else :
            gold_list.append(gold_line.strip('\n'))# if only one hypernym add it to list
        for hyper in gold_list: #for each hypernym in list
            hyper.rstrip('\n')
            writer.writerow([hypo,hyper]) #write hyponym<\t>hypernym for each hypernym
            
file_ptr_gold.close()
file_ptr_in.close()
