#!/bin/bash
model=$1
python create_hypo_hyper_list_from_train_data.py
python dictionary.ru.py --w2v $model
python  prepare.py --w2v $model >preplog
python  cluster.py
python train.py > trainlog
python evaluate1.py --w2v $model --non_optimized ./ > evalOut1
python identity1.py --w2v $model > idenOut1
python evaluate2.py --w2v $model --non_optimized ./ > evalOut2
python identity2.py --w2v $model > idenOut2
python evaluate3.py --w2v $model --non_optimized ./ > evalOut3
python identity3.py --w2v $model > idenOut3
python refine_candidates.py baseline_test_candidates1  baseline_test_candidates1_refine
python refine_candidates.py baseline_test_candidates2  baseline_test_candidates2_refine
python refine_candidates.py baseline_test_candidates3  baseline_test_candidates3_refine
python refine_candidates.py i_test_candidates1  i_test_candidates1_refine
python refine_candidates.py i_test_candidates2  i_test_candidates2_refine
python refine_candidates.py i_test_candidates3  i_test_candidates3_refine
python task9-scorer.py test_gold1 baseline_test_candidates1_refine > result_eval1
python task9-scorer.py test_gold2 baseline_test_candidates2_refine > result_eval2
python task9-scorer.py test_gold3 baseline_test_candidates3_refine > result_eval3
python task9-scorer.py i_test_gold1 i_test_candidates1_refine > result_i1
python task9-scorer.py i_test_gold2 i_test_candidates2_refine > result_i2
python task9-scorer.py i_test_gold3 i_test_candidates3_refine > result_i3

