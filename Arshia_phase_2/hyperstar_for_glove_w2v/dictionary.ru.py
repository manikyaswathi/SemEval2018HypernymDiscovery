#!/usr/bin/env python

import argparse
import csv
import random
import gensim
from collections import defaultdict
import numpy as np
try:
    from sklearn.model_selection import train_test_split
except ImportError:
    from sklearn.cross_validation import train_test_split

parser = argparse.ArgumentParser(description='Russian Dictionary.')
parser.add_argument('--w2v',  default='w2v.txt', nargs='?', help='Path to the word2vec model.')
parser.add_argument('--seed', default=228, type=int, nargs='?', help='Random seed.')#seed for random sampling of data
args = vars(parser.parse_args())

RANDOM_SEED = args['seed']
random.seed(RANDOM_SEED)

w2v = gensim.models.KeyedVectors.load_word2vec_format(args['w2v'], binary=True, unicode_errors='ignore')
w2v.init_sims(replace=True)

hypernyms_patterns   = defaultdict(lambda: list())

with open('data_train_gold.csv') as f:
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)    
    for row in reader:
        hyponym, hypernym = row['hyponym'], row['hypernym']
        if hyponym in w2v and hypernym in w2v and hypernym not in hypernyms_patterns[hyponym]:
            hypernyms_patterns[hyponym].append(hypernym)            

keys_hypernyms_patterns = [k for k in hypernyms_patterns.keys() if len(hypernyms_patterns[k]) > 0]

hypernyms_patterns_train, hypernyms_patterns_validation_test = train_test_split(np.arange(len(keys_hypernyms_patterns), dtype='int32'), test_size=.4, random_state=RANDOM_SEED)
hypernyms_patterns_validation, hypernyms_patterns_test = train_test_split(hypernyms_patterns_validation_test, test_size=.5, random_state=RANDOM_SEED)

hypernyms_train = {k: hypernyms_patterns[k] for i in hypernyms_patterns_train for k in (keys_hypernyms_patterns[i],)}
for hyponym, hypernyms in hypernyms_patterns.items():
    if hyponym in hypernyms_train:
        for hypernym in hypernyms:
            if not hypernym in hypernyms_train[hyponym]:
                hypernyms_train[hyponym].append(hypernym)

hypernyms_validation = {k: hypernyms_patterns[k] for i in hypernyms_patterns_validation for k in (keys_hypernyms_patterns[i],)}
hypernyms_test       = {k: hypernyms_patterns[k] for i in hypernyms_patterns_test       for k in (keys_hypernyms_patterns[i],)}

subsumptions_train      = [(x, y) for x, ys in hypernyms_train.items()      for y in ys]
subsumptions_validation = [(x, y) for x, ys in hypernyms_validation.items() for y in ys]
subsumptions_test       = [(x, y) for x, ys in hypernyms_test.items()       for y in ys]

def write_subsumptions(subsumptions, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f, dialect='excel-tab', lineterminator='\n')
        for pair in subsumptions:
            writer.writerow(pair)

write_subsumptions(subsumptions_train,      'subsumptions-train.txt')
write_subsumptions(subsumptions_validation, 'subsumptions-validation.txt')
write_subsumptions(subsumptions_test,       'subsumptions-test.txt')
