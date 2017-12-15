# -*- coding: utf-8 -*-
# Rank metrics from https://gist.github.com/bwhite/3726239
import sys
import numpy as np

def mean_reciprocal_rank(rs):
    """Score is reciprocal of the rank of the first relevant item
    First element is 'rank 1'.  Relevance is binary (nonzero is relevant).
    Example from http://en.wikipedia.org/wiki/Mean_reciprocal_rank
    >>> rs = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    >>> mean_reciprocal_rank(rs)
    0.61111111111111105
    >>> rs = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0]])
    >>> mean_reciprocal_rank(rs)
    0.5
    >>> rs = [[0, 0, 0, 1], [1, 0, 0], [1, 0, 0]]
    >>> mean_reciprocal_rank(rs)
    0.75
    Args:
        rs: Iterator of relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Mean reciprocal rank
    """
    rs = (np.asarray(r).nonzero()[0] for r in rs)
    return np.mean([1. / (r[0] + 1) if r.size else 0. for r in rs])


def r_precision(r):
    """Score is precision after all relevant documents have been retrieved
    Relevance is binary (nonzero is relevant).
    >>> r = [0, 0, 1]
    >>> r_precision(r)
    0.33333333333333331
    >>> r = [0, 1, 0]
    >>> r_precision(r)
    0.5
    >>> r = [1, 0, 0]
    >>> r_precision(r)
    1.0
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        R Precision
    """
    r = np.asarray(r) != 0
    z = r.nonzero()[0]
    if not z.size:
        return 0.
    return np.mean(r[:z[-1] + 1])


def precision_at_k(r, k):
    """Score is precision @ k
    Relevance is binary (nonzero is relevant).
    >>> r = [0, 0, 1]
    >>> precision_at_k(r, 1)
    0.0
    >>> precision_at_k(r, 2)
    0.0
    >>> precision_at_k(r, 3)
    0.33333333333333331
    >>> precision_at_k(r, 4)
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Relevance score length < k
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Precision @ k
    Raises:
        ValueError: len(r) must be >= k
    """
    assert k >= 1
    r = np.asarray(r)[:k] != 0
    if r.size != k:
        raise ValueError('Relevance score length < k')
    return np.mean(r)


def average_precision(r):
    """Score is average precision (area under PR curve)
    Relevance is binary (nonzero is relevant).
    >>> r = [1, 1, 0, 1, 0, 1, 0, 0, 0, 1]
    >>> delta_r = 1. / sum(r)
    >>> sum([sum(r[:x + 1]) / (x + 1.) * delta_r for x, y in enumerate(r) if y])
    0.7833333333333333
    >>> average_precision(r)
    0.78333333333333333
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Average precision
    """
    r = np.asarray(r) != 0
    out = [precision_at_k(r, k + 1) for k in range(r.size) if r[k]]
    if not out:
        return 0.
    return np.mean(out)


def mean_average_precision(rs):
    """Score is mean average precision
    Relevance is binary (nonzero is relevant).
    >>> rs = [[1, 1, 0, 1, 0, 1, 0, 0, 0, 1]]
    >>> mean_average_precision(rs)
    0.78333333333333333
    >>> rs = [[1, 1, 0, 1, 0, 1, 0, 0, 0, 1], [0]]
    >>> mean_average_precision(rs)
    0.39166666666666666
    Args:
        rs: Iterator of relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Mean average precision
    """
    return np.mean([average_precision(r) for r in rs])


def get_hypernyms(line, is_gold=True):
    if is_gold == True:
        valid_hyps = line.strip().decode('utf-8').split('\t')
        return valid_hyps
    else:
        linesplit=line.strip().decode('utf-8').split('\t')
        cand_hyps=[]
        for hyp in linesplit[:limit]:
            hyp_lower=hyp.lower()
            if hyp_lower not in cand_hyps: cand_hyps.append(hyp_lower)
        return cand_hyps

if __name__ == '__main__':

    args = sys.argv[1:]

    if len(args) == 2:

        limit=15
        gold = args[0]
        predictions = args[1]

        fgold = open(gold, 'r')
        fpredictions = open(predictions, 'r')

        goldls = fgold.readlines()
        predls = fpredictions.readlines()

        if len(goldls)!=len(predls): sys.exit('ERROR: Number of lines in gold and output files differ')

        all_scores = []
        scores_names = ['MRR', 'MAP', 'R-P', 'P@1', 'P@5', 'P@15']
        for i in range(len(goldls)):

            goldline = goldls[i]
            predline = predls[i]
            
            avg_pat1 = []
            avg_pat2 = []
            avg_pat3 = []
            avg_pat4 = []
            avg_pat5 = []
            avg_rprec = []
            rs = []


            gold_hyps = get_hypernyms(goldline, is_gold=True)
            pred_hyps = get_hypernyms(predline, is_gold=False)
            gold_hyps_n = len(gold_hyps)
            r = [0 for i in range(limit)]

            for j in range(len(pred_hyps)):
                if j <= gold_hyps_n:
                    pred_hyp = pred_hyps[j]
                    if pred_hyp in gold_hyps:
                        r[j] = 1

            rs.append(r)
            avg_pat1.append(precision_at_k(r,1))
            avg_pat2.append(precision_at_k(r,5))
            avg_pat3.append(precision_at_k(r,15))
            avg_rprec.append(r_precision(r))


            mrr_score_numb = mean_reciprocal_rank(rs)
            map_score_numb = mean_average_precision(rs)
            avg_pat1_numb = sum(avg_pat1)/len(avg_pat1)
            avg_pat2_numb = sum(avg_pat2)/len(avg_pat2)
            avg_pat3_numb = sum(avg_pat3)/len(avg_pat3)
            avg_rprec_numb = sum(avg_rprec)/len(avg_rprec)
            
            scores_results = [mrr_score_numb, map_score_numb, avg_rprec_numb, avg_pat1_numb, avg_pat2_numb, avg_pat3_numb]        
            all_scores.append(scores_results)


        for k in range(len(scores_names)):
            print scores_names[k]+': '+str(sum([score_list[k] for score_list in all_scores]) / len(all_scores))




    else:
        sys.exit('Argument: (1) Gold file; (2) Predictions file')
