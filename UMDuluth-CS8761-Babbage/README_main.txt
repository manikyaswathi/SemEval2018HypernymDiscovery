Team Babbage : CS 8761 Project
SemEval-2018 Task 9: Hypernym Discovery

File Created By : Arshia
File Modified By : Swathi

********************************************************************
*   DO NOT REMOVE FILES LISTED IN THE README OF ALL THE FOLDER     *
********************************************************************

Task objective : Given a hyponym generate a ranked list of candidate hypernyms from a vocabulary set.
----------------
Corpus: UMBC WebBase Corpus http://ebiquity.umbc.edu/blogger/2013/05/01/umbc-webbase-corpus-of-3b-english-words/ 
-------
Ideas Implemented from Reference papers:
1. Co-occurance on Bag of Words : https://arxiv.org/pdf/1603.08702.pdf
2. Hearst Patterns : http://people.ischool.berkeley.edu/~hearst/papers/coling92.pdf
3. Learning Semantic Hierarchies via Word Embeddings : https://www.aclweb.org/anthology/P/P14/P14-1113.xhtml 
4. word2Vec : Efficient Estimation of Word Representations in Vector Space https://arxiv.org/pdf/1301.3781.pdf 
============================================================================================================================
Project Overview :
--------------------
The complete system consists of four independent sub-systems.
----------------------------------------------------------------------------------
First two sub-systems were dveloped in the stage 1 of development period. 
The last two systems were developed in the stage 2 of development period.
----------------------------------------------------------------------------------
Sub-system 1. Stage 1 Normalization - co-occurrence frequencies @ Stage1_Babbage
-------------
Sub-system 2. Stage 1 Hearst Pattersm - co-occurrence frequencies @ Stage1_Babbage
------------- [ Sub-system 1. and Sub-system 2. @ Stage1_Babbage - used Install.sh inside thos folder to extract the Stage 1 and use runIt.sh from inside the extrected folder ] Otherwise these resulls are copied under System_Babbage/src/Merge
Sub-system 3. Stage 2 Model 1 @ System_Babbage/src/BuildModel1
-------------
Sub-system 4. Stage 2 Model 2 - PHI Module @ System_Babbage/src/PHIModule
-------------
Merge : The Results of all the above sub-systems are merged and scored using runMergeEval.sh @ System_Babbage/src/Merge/
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sub-system 1.
--------------
	Generates candidate hypernyms based on cooccurrance frequencies of input hyponym and phrases within a line.
Example of normalized data produced for sub-system 1 - 
	starvation void approval desire food times urge    the_desire pounding_urge desire_for_food a_void
Original data - 
	''_'' ..._: starvation_NN fills_VBZ a_DT void_NN inside_IN when_WRB it_PRP 's_VBZ approval_NN from_IN you_PRP I_PRP crave_VBP ._. The_DT desire_NN for_IN food_NN is_VBZ gone_VBN and_CC you_PRP are_VBP there_RB again_RB ..._: yelling_VBG ..._: so_RB negative_JJ ._. Times_NNP like_IN this_DT filled_VBN with_IN the_DT pounding_VBG urge_NN to_TO run_VB far_RB away_RB and_CC disappear_VB ..._: ''_''
Here, if "desire" is a hyponym all phrases within that line are considered as potential hypernyms and ranked using cooccurrance frequency. 	
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++	
Sub-system 2.
-------------
	Generates candidate hypernyms based on cooccurrance frequencies of hyponym-hypernym pairs extracted using Hearst patterns.
Example of normalized data produced for sub-system 2 using Hearst pattern "such as" - 
	disease : brain_tumor  (hypernym : hyponym )
Original data snippet - 
 ...disease_NN such_JJ as_IN brain_NN tumor_NN ...
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sub-system 3.
-------------
CREATED BY : SWATHI
====================
	Generates candidate hypernyms from hyponym-hypernym pairs extracted using "IS-A" pattern and considering sub-phrases within hyponym as possible hypernym
Example of sub-phrase selection :
	"department" is a possible hypernym of hyponym "sociology department"
Example of data extracted using IS-A pattern :
	sucralose : artificial_sweetener (hyponym : hypernym)
Original data snippet -
	Sucralose_NNP is_VBZ an_DT artificial_JJ sweetener_NN ... 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sub-system 4.
--------------
Reserach: As part of this stage Arshia conducted few experiments.
--------                        -----
1. analysing and creating GloVe Vector.
2. hyper-star project implemented based on Learning Semantic Hierarchies via Word Embeddings : https://www.aclweb.org/anthology/P/P14/P14-1113.xhtml. [Third-Part-Tools : report_hyperstar_arshia.tx ]
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////   	THE ACTUAL IMPLEMEMTATION  /////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                        IMPLEMENTED BY : SWATHI
                                        =======================
Generates candidate hypernyms from word-embeddings trained using normalized data corpus and using the following formulas:
	  - most_smilar(POSITIVE, NEGATIVE, n) : 2 set of results to get the Hypernym of X=Input_word
	    phi1 = POSITIVE=[Input_Word, PHI * Input_Word]  NEGATIVE=[]
	    phi2 = POSITIVE=[Input_Word]  NEGATIVE=[PHI * Input_Word]
	    **************************************************************************************************
	    	   	           PHI * Input_Word                    PHI * Input_Word
	    	<Hypernym_List><------------------------ Input_Word ----------------------><Hypernym_List>
	<-----------------------------------------------Vector Space-------------------------------------------->
	    **************************************************************************************************
Word Embeddings - [ Efficient Estimation of Word Representations in Vector Spacehttps://arxiv.org/pdf/1301.3781.pdf ]
     		    	**************************************************************
                        PHI* (or PHI) = arg-min[phi: 1→ N]  ((1/N) ∑|| phi*X – Y ||^2)
			**************************************************************
[Formula 1 from Learning Semantic Hierarchies via Word Embeddings : https://www.aclweb.org/anthology/P/P14/P14-1113.xhtml]
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The results from the sub-system are merges as follows:
    	    RESULT = {Sub-system 3. + [(Sub-system 1. + Sub-system 2.) + Sub-system 1.]}
	    RESULT_CONCEPT = Concepts of RESULTS
	    RESULT_ENTITY  = Entities of RESULTS 

The sample results:
===================
1. RESULTS FOR: Module 1 + (STAGE 1 + PHI MODULE) [FINAL] RESULTS
*****************************************************************
 MRR: 0.1514500074
 MAP: 0.145593864161
 R-P: 0.139695247345
 P@1: 0.112
 P@5: 0.0476
 P@15: 0.0213777777778
 SEPARATING [FINAL] RESULTS
 SEPARATING [GOLD] DATA
2. RESULTS FOR: Module 1 + (STAGE 1 + PHI MODULE) [FINAL] CONCEPT RESULTS
**************************************************************************
 MRR: 0.177263478208
 MAP: 0.171514316841
 R-P: 0.165660196687
 P@1: 0.126659856997
 P@5: 0.0574055158325
 P@15: 0.0262853251617
3. RESULTS FOR: Module 1 + (STAGE 1 + PHI MODULE) [FINAL] ENTITY RESULTS
**************************************************************************
 MRR: 0.102944464365
 MAP: 0.0968872937683
 R-P: 0.0909050642256
 P@1: 0.084452975048
 P@5: 0.0291746641075
 P@15: 0.0121561100448
=========================================================================
       
