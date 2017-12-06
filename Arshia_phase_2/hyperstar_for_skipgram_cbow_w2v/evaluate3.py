#!/usr/bin/env python
from batch_sim.nn_vec import nn_vec
import argparse
import csv
import glob
import os
import pickle
import re
import sys
import gensim
from collections import defaultdict
import numpy as np
from projlearn import MODELS
from multiprocessing import cpu_count

parser = argparse.ArgumentParser(description='Evaluation.')
parser.add_argument('--w2v',          default='w2v.txt', nargs='?', help='Path to the word2vec model.')
parser.add_argument('--test',         default='test.npz',              nargs='?', help='Path to the test set.')
parser.add_argument('--subsumptions', default='subsumptions-test.txt', nargs='?', help='Path to the test subsumptions.')
parser.add_argument('--non_optimized', action='store_true', help='Disable most similar words calculation optimization.')
parser.add_argument('--threads',       nargs='?', type=int, default=cpu_count(), help='Number of threads.')
parser.add_argument('path', nargs='*', help='List of the directories with results.')
args = vars(parser.parse_args())

if not len(sys.argv) > 1:
    print('Usage: %s path...' % (sys.argv[0]))
    sys.exit(1)

WD = os.path.dirname(os.path.realpath(__file__))

w2v = gensim.models.KeyedVectors.load(os.path.join(WD, args['w2v']))
w2v.init_sims(replace=True)

with np.load(args['test']) as npz:
    X_index_test  = npz['X_index']
    Y_all_test    = npz['Y_all']
    Z_all_test    = npz['Z_all']

X_all_test  = Z_all_test[X_index_test[:, 0],   :]

subsumptions_test = []

with open(args['subsumptions']) as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

    for row in reader:
        subsumptions_test.append((row[0], row[1]))

assert len(subsumptions_test) == X_all_test.shape[0]

def extract(clusters, Y_hat_clusters):
    cluster_indices = {cluster: 0 for cluster in Y_hat_clusters}

    Y_all_hat = []

    for cluster in clusters:
        Y_hat = Y_hat_clusters[cluster][cluster_indices[cluster]]
        cluster_indices[cluster] += 1

        Y_all_hat.append(Y_hat)

    assert sum(cluster_indices.values()) == len(clusters)

    return np.array(Y_all_hat)

def compute_ats(measures):
    return [sum(measures[j].values()) / len(subsumptions_test) for j in range(len(measures))]

def compute_auc(ats):
    return sum([ats[j] + ats[j + 1] for j in range(0, len(ats) - 1)]) / 2

def sort_list(hypernym_dict) :
    sorted_candidates = list()
    for word in sorted(hypernym_dict, key=hypernym_dict.get, reverse=True):
    	sorted_candidates.append(word)
    return sorted_candidates

for path in args['path']:
    print('Doing "%s" on "%s" and "%s".' % (path, args['test'], args['subsumptions']))

    kmeans = pickle.load(open(os.path.join(path, 'kmeans.pickle'), 'rb'))
    print('The number of clusters is %d.' % (kmeans.n_clusters))

    clusters_test  = kmeans.predict(Y_all_test - X_all_test)

    for model in MODELS:
        try:
            with np.load(os.path.join(path, '%s.test.npz') % model) as npz:
                Y_hat_clusters = {int(cluster): npz[cluster] for cluster in npz.files}
        except FileNotFoundError:
            Y_hat_clusters = {}

        if kmeans.n_clusters != len(Y_hat_clusters):
            print('Missing the output for the model "%s"!' % model)
            continue

        Y_all_hat = extract(clusters_test, Y_hat_clusters)

        assert len(subsumptions_test) == Y_all_hat.shape[0]

        measures = [{} for _ in range(10)]

        if not args['non_optimized']:
            # normalize Y_all_hat to make dot product equeal to cosine and monotonically decreasing function of euclidean distance
            Y_all_hat_norm = Y_all_hat / np.linalg.norm(Y_all_hat,axis=1)[:,np.newaxis]
            print('nn_vec...')
            similar_indices = nn_vec(Y_all_hat_norm, w2v.syn0norm, topn=10, sort=True, return_sims=False, nthreads=args['threads'], verbose=False)
            print('nn_vec results covert...')
            similar_words = [[w2v.index2word[ind] for ind in row] for row in similar_indices]
            print('done')
        file_ptr_ms = open(str(model)+"_test_candidates3",'w')
        file_ptr_hypo = open("test_hypo3",'w')
        file_ptr_gold = open("test_gold3",'w')
        prev_hypo = ''
        gold_list = ''
        out_ms = ''
	count = 0
	temp_hyper_list = {}
        for i, (hyponym, hypernym) in enumerate(subsumptions_test):
            if args['non_optimized']:
                Y_hat  = Y_all_hat[i].reshape(X_all_test.shape[1],)
                actual = [w for w,_ in w2v.most_similar(positive=[Y_hat], topn=10)]
            else:
                actual = similar_words[i]
			
            if count==0 or prev_hypo == hyponym :
                gold_list = gold_list + hypernym + '\t'
                for word in actual:
			if word not in temp_hyper_list.keys() :
				temp_hyper_list[word]=1
			else:
				temp_hyper_list[word]+=1
                prev_hypo = hyponym
		count = 1
            elif prev_hypo != hyponym :                
                gold_list = gold_list + '\n'
		sorted_hyper_list = sort_list(temp_hyper_list)
		for word in sorted_hyper_list :
			out_ms = out_ms + str(word) + "\t"
		out_ms = out_ms + '\n'
                file_ptr_ms.write(out_ms)
                file_ptr_hypo.write(prev_hypo + '\n')
                file_ptr_gold.write(gold_list)
				
                gold_list = ''
                out_ms = ''
		temp_hyper_list={}
				
                prev_hypo = hyponym
                gold_list = gold_list + hypernym + '\t'
                for word in actual:
                        if word not in temp_hyper_list.keys() :
                                temp_hyper_list[word]=1
                        else:
                                temp_hyper_list[word]+=1
                
            for j in range(0, len(measures)):
                measures[j][(hyponym, hypernym)] = 1. if hypernym in actual[:j + 1] else 0.

            if (i + 1) % 100 == 0:
                ats = compute_ats(measures)
                auc = compute_auc(ats)
                ats_string = ', '.join(['A@%d=%.6f' % (j + 1, ats[j]) for j in range(len(ats))])
                print('%d examples out of %d done for "%s/%s": %s. AUC=%.6f.' % (
                    i + 1,
                    len(subsumptions_test),
                    path,
                    model,
                    ats_string,
                    auc))
        file_ptr_ms.close()
	file_ptr_hypo.close()
	file_ptr_gold.close()
        ats = compute_ats(measures)
        auc = compute_auc(ats)
        ats_string = ', '.join(['A@%d=%.4f' % (j + 1, ats[j]) for j in range(len(ats))])
        print('For "%s/%s": overall %s. AUC=%.6f.' % (
            path,
            model,
            ats_string,
            auc))
