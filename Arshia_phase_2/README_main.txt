Team Babbage : CS 8761 Project
SemEval-2018 Task 9: Hypernym Discovery

Task objective : Given a hyponym generate a ranked list of candidate hypernyms from a vocabulary set.

Corpus: 

Ideas Implemented from Reference papers:
1. Co-occurance on Bag of Words : https://arxiv.org/pdf/1603.08702.pdf
2. Hearst Patterns : http://people.ischool.berkeley.edu/~hearst/papers/coling92.pdf
3. 

Project Overview :
The complete system consists of four independent sub-systems.
First two sub-systems were dveloped in the stage 1 of development period. 
The last two systems were developed in the stage 2 of development period.
Sub-system 1. 
Sub-system 2.
Sub-system 3.
Sub-system 4.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sub-system 1. 
	Generates candidate hypernyms based on cooccurrance frequencies of input hyponym and phrases within a line.
Example of normalized data produced for sub-system 1 - 
	starvation void approval desire food times urge    the_desire pounding_urge desire_for_food a_void
Original data - 
	''_'' ..._: starvation_NN fills_VBZ a_DT void_NN inside_IN when_WRB it_PRP 's_VBZ approval_NN from_IN you_PRP I_PRP crave_VBP ._. The_DT desire_NN for_IN food_NN is_VBZ gone_VBN and_CC you_PRP are_VBP there_RB again_RB ..._: yelling_VBG ..._: so_RB negative_JJ ._. Times_NNP like_IN this_DT filled_VBN with_IN the_DT pounding_VBG urge_NN to_TO run_VB far_RB away_RB and_CC disappear_VB ..._: ''_''
Here, if "desire" is a hyponym all phrases within that line are considered as potential hypernyms and ranked using cooccurrance frequency. 	
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++	
Sub-system 2.
	Generates candidate hypernyms based on cooccurrance frequencies of hyponym-hypernym pairs extracted using Hearst patterns.
Example of normalized data produced for sub-system 2 using Hearst pattern "such as" - 
	disease : brain_tumor  (hypernym : hyponym )
Original data snippet - 
 ...disease_NN such_JJ as_IN brain_NN tumor_NN ...
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sub-system 3.
	Generates candidate hypernyms from hyponym-hypernym pairs extracted using "IS-A" pattern and considering sub-phrases within hyponym as possible hypernym
Example of sub-phrase selection :
	"department" is a possible hypernym of hyponym "sociology department"
Example of data extracted using IS-A pattern :
	sucralose : artificial_sweetener (hyponym : hypernym)
Original data snippet -
	Sucralose_NNP is_VBZ an_DT artificial_JJ sweetener_NN ... 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sub-system 4.
	Generates candidate hypernyms from word-embeddings trained using normalized data corpus and using the following formulas :

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++