Team Babbage : CS 8761 Project
SemEval-2018 Task 9: Hypernym Discovery

Author: Manikya Swathi Vallabhajosyula

Problem: Identifying the set of candidate hypernyms (from a vobulary of hypernyms) for the given input term (hyponym)

Corpus: UMBC tagged corpus [https://drive.google.com/file/d/0Bz40_IukD5qDUGVhMURFWE9aYVU/view]
Pre-processed Corpus: Normalised and Hearts Patterns [https://drive.google.com/a/d.umn.edu/file/d/0B9xD1bj5DY-GUG1raDJzelNvRU0/view?usp=sharing]
Input: Input Term list (trial) - 50 words
Lookup: A list of vocab candidate hypernym words - 218759 words

Ideas Implemented from Reference papers:
1. Co-occurance on Bag of Words : https://arxiv.org/pdf/1603.08702.pdf
2. Hearst Patterns : http://people.ischool.berkeley.edu/~hearst/papers/coling92.pdf

Description:
This system is implemmeted in three Sections:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
PART 1 - SECTION A [swathi]: Preprocessing Data - PATTERN 1 & 2
PART 1 - SECTION B [arshia]: Obatining Coocurance counts and count extraction from PATTERN 1 & 2
PART 1 - SECTION C [swathi]: Score the Output and Structre the project
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
PART 1. The Process Description		
====================================================================================================================
SECTION A.	Patterns for our system									[Swathi]
Look for the Swathi_project_report.txt for more details
====================================================================================================================
PATTERN 1: Bag-of-words cococcurance - per line
---------- Example ----------------------------
INPUT :
-------
``_`` The_DT DeLorme_NNP PN-20_NNP represents_VBZ a_DT new_JJ breed_NN of_IN GPS_NNP devices_NNS ._. ..._: a_DT fantastic_JJ device_NN ,_, and_CC it_PRP leads_VBZ the_DT way_NN in_IN a_DT new_JJ breed_NN of_IN GPS_NNP devices_NNS which_WDT can_MD display_VB aerial_JJ photography_NN and_CC satellite_NN imagery_NN ._. For_IN people_NNS who_WP have_VBP dreamed_VBN about_IN having_VBG a_DT Google_NNP Earth_NNP type_NN product_NN in_IN a_DT handheld_JJ device_NN ..._: this_DT is_VBZ it_PRP ._. ''_''

OUTPUT : bi-gram-trigrams with NN POS tags, unigrams with NN[A-Z]* POS tags
---------------------------------------------------------------------------
delorme pn-20 breed gps devices device way breed gps devices photography satellite imagery people google earth type product device    photography_and_satellite handheld_device new_breed breed_of_gps satellite_imagery aerial_photography the_way the_delorme gps_devices google_earth_type earth_type fantastic_device a_google
*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
PATTERN 2: Hearsts Patters - with in sentence boundaries
---------- Example ----------------------------
INPUT :
-------
Those_DT who_WP are_VBP suffering_VBG with_IN this_DT illness_NN have_VBP a_DT low_JJ self-esteem_NN and_CC often_RB a_DT tremendous_JJ need_NN to_TO control_VB their_PRP$ surroundings_NNS and_CC emotions_NNS ._. The_DT Eating_NNP Disorder_NNP ,_, Anorexia_NNP ,_, is_VBZ a_DT unique_JJ reaction_NN to_TO a_DT variety_NN of_IN external_JJ and_CC internal_JJ conflicts_NNS ,_, such_JJ as_IN stress_NN ,_, anxiety_NN ,_, unhappiness_NN and_CC feeling_NN like_IN life_NN is_VBZ out_IN of_IN control_NN ._. 

OUTPUT : Noun Phrase patters in HEARTS
--------------------------------------------
internal_conflicts : stress , anxiety , unhappiness , feeling 
====================================================================================================================
SECTION B.	Building the maps and Output candicate Hypernyms					[Arshia]
Look for Arshia_project_report.txt for more details
====================================================================================================================
From the Normalised text and Hearst patterns two differnt modules are run to create the output files:
The Intremedita Map File would look like the following for one input word:
******************************************************************
don mckellar : particular_day	1 , uicide	2 , hanging	2 , the_movie	4 , conceit_of_writer-director	1 , a_repertoire	1 , brilliant_two-disc_hodgepodge	1 , amuel	2 , ale	1 , the_world	3 , aids-afflicted_musician	1 , teve_murray	2 , ..............................................................................................................................
.........................................................................................................................................................................................................................................................................................,  gutter_level	1 , boot	1 , ouimette	2 , book	1 , oar	1 , music_during_china	1 , dvd_commentary	1 , uave_cube-neighbor	1 , junk	1 , loved_one	1 , variation	1 , ibling	1 , foil	1 , container	1 , epilogue	1 , my$	1 , goin	2 , ghost	1 , writer-director_don_mckellar	2 , truggle	1 , a_game-tester	1 , featuring_mcdonald	1 , 
******************************************************************
From the above mapping the input term is looked up and a the cadidate hypernyms are fetched from the vocab file and output file is created:
*******************************************************************
dirham	morocco	thou	day	price	abu	government	king	country	money	bank	o	market	dollar	exchange	hand	dinar	gold	thee	city	rate	moroccan	oil	thy	case	month	hop	coin	world	court	weight	worker	dyer	paper	rite	u	barber	tate	clothe	ape	cost	account	end	folk	way	ir	charge	fire	budget	night	friend	article	pain	fine	growth	right	worth	muslim	men	cheese	cook	brother	porter	hotel	the_end	master	project	life	the_city	investment	taxi	debt	economy	cent	eye	wage	report	passenger	fisherman	pot	golf	person	age	owner	caliph	monarchy	everything	demand	purse	door	transaction	meat	morning	company	lord	agreement	pound	letter	prison	tore	euro	payment	effect	france	merchant	level	islamic	term	inflation	nothing	journal	member	damage	gdp	banking	river	problem	reserve	arab	appeal	club	increase	ifc	u.s.	root	round	girl	lave	companion	none	fish	bit	arabic	musa	gift	contract	fee	emirate	larrikin	desire	tory	minister	tail	hast	fund	drug	rule	manner	cone	teacher	ea	vehicle	tasse	interest	vegetable	form	may	remuneration	infrastructure	middle	chamber	airport	town	honor	center	current_account	dye	week	thursday	prophet	the_prophet	income	april	empire	passport	joseph	resource	allowance	rest	loan	un	hunger	valley	integrity	dyery	war	trial	half	provision	the_street	import	central	the_paper	pace	ide	measure	quarter	ne'er	permit	luck	keeper	wealth	mad	finance	living	hour	desert	croll	reform	judgment	foreign_e
***************************************************************************************************************
====================================================================================================================
SECTION C.	Building The struncture and Output analysis					[Swathi]
====================================================================================================================
UMDuluth-CS8761-Babbage
	|_ Output
		|_ 1A.english.output.trial.hearst-Stage1_sample.txt  
		|_ 1A.english.output.trial.norm-stage1_Sample.txt    	
		|_ 1A.english.output.trial.merge-stage1_Sample.txt   
		|_ ReadMe.txt
	|_ Sample_Runs						[Should be copied outside this folder to run]
		|_ ReadMe.txt 
		|_ runIt_FromNoramlText.sh  
		|_ runIt_QuickRun.sh
	|_ UMBC_Sample_Corpus					[Sample files 1 from each domain just for test run]
		|_ delorme.com_shu.pages_11.possf2  
		|_ ucdavis_wnba.pages_11.possf2  
		|_ weather.yahoo_bbk.ac.pages_11.possf2
		|_ mbta.com_mtu.pages_11.possf2     
		|_ utexas_iit.pages_11.possf2
	|_ src
		|_ cooc.py                   			[arshia]         
		|_ generate_cooc_to_file.py                     [arshia]
		|_ hearst_generate_candidate_load_map.py        [arshia]
		|_ mergeOutput.py				[swathi]
		|_ getTags.py                                   [swathi]
		|_ hearst_generate_cooc_to_file.py        	[arshia]
		|_ Readme.txt						
		|_ generate_candidate_from_corpus.py  		[arshia]
		|_ HearstAlgo_Norm.py                        	[swathi]
		|_ hearst.py					[arshia]
		|_ generate_candidate_load_map.py     		[arshia]
		|_ hearst_generate_candidate_from_corpus.py  	[arshia]
	|_ SemEval18-Task9					[Available Data - with minimal processing]
		|_ README.txt  
		|_ task9-scorer.py  
		|_ trial
			|_ data
				|_ 1A.english.trial.data_H.txt  
				|_ 1A.english.trial.data_N.txt
  			|_ gold
				|_ 1A.english.trial.gold.txt
		|_ training
			|_ data
				|_ 1A.english.training.data_H.txt  
				|_ 1A.english.training.data_N.txt
			|_ gold
				|_ 1A.english.training.gold.txt
		|_ vocabulary
			|_ 1A.english.vocabulary_0.txt  
			|_ 1A.english.vocabulary_1.txt  
			|_ 1A.english.vocabulary.txt  
			|_ 1A.english.vocabulary.under.txt  
			|_ ReadMe.txt
	|_ temp
		|_ Maps
			|_ 1A.english.train.cooccur.map.txt	[Just a Place Holder]  
			|_ 1A.english.train.hearst.map.txt  	[arshia]
			|_ 1A.english.trial.cooccur.map.txt  	[arshia]
			|_ 1A.english.trial.hearst.map.txt	[arshia]
		|_ DataN	[Empty for future]
		|_ DataH	[Empty for future]
		|_ store	[Empty for future]
	|_ Arshia_project_report.txt		[swathi]
	|_ Swathi_project_report.txt		[arshia]
	|_ RESULTS-Stage1_Sample.TXT	
	|_ RESULTS.TXT				[swathi]
	|_ DetailsOf_runIT_sh.txt		[swathi]
	|_ runIt.sh                             [swathi]    
        |_ Main_ReadMe.txt			[Current File]
===============================================================================================================
The results: run as -
> python task9-scorer.py [a] [b]
--------------------------------------------------------------------------------------------------------------
|_ Output
		|_ 1A.english.output.trial.hearst-Stage1_sample.txt  [1]
		|_ 1A.english.output.trial.norm-stage1_Sample.txt    [2]	
		|_ 1A.english.output.trial.merge-stage1_Sample.txt   [3]
|_ SemEval18-Task9					[Available Data - with minimal processing]
		|_ README.txt  
		|_ task9-scorer.py  
		|_ trial
			|_ data
				|_ 1A.english.trial.data_H.txt  
				|_ 1A.english.trial.data_N.txt
  			|_ gold
				|_ 1A.english.trial.gold.txt         [4]

The scoreer program is run as : see the sample results RESULTS-Stage1_Sample.TXT
#. [a] ----- [b]
1. [4] ----- [1]
2. [4] ----- [2]
3. [4] ----- [3]
		
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Part 2 : FLow Graph
===============================================================================================================
  					    OVERALL SYSTEM
				 ---------------------------------------
				|					|	
				| 1. 1A.english.vocabulary.under.txt	|	1. RESULTS.txt	
				| 2. 1A.english.trial.gold.txt		|	2. Output/1A.english.output.trial.hearst.txt
  Input Vocab			| 3. 1A.english.vocabulary.under.txt	|	3. Output/1A.english.output.trial.norm.txt
  [Trail-50 Terms]	     ==>| 4. UMBC tagged corpus (or)		|==>	4. Output/1A.english.output.trial.merge.txt
     				|    Pre-Processed data (or)		|
 1A.english.trial.data_H.txt	|    mapped files			|
 1A.english.trial.data_N.txt	|    a. 1A.english.trial.cooccur.map.txt|
				|    b. 1A.english.trial.hearst.map.txt |
				|					|
				 ---------------------------------------

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ANALYSIS: Repetation from file: Swathi_project_report.txt
-----------------------------------------------------------
Running the score program againt all files in Output folder. ANALYSIS:
> result with "1A.english.output.trial.norm-Stage1_sample.txt" seem to get MRR 0.26 over 1.0.
- seem to get a fairly good result with just one feature (co-occurance) over all the sample putput files (not just 15)
- This could improve if we would add more feature to the candidate hypernym extraction algorithm
> result with "1A.english.output.trial.hearst-Stage1_sample.txt" seem to get MRR 0.00333333333333 over 1.0.
- This is very poor as we have not yet applied unigrams, bigrams and trigrams from the hearst patterns.
- we plainly match the NP from the HEARST PATTERNS to the vaocabulary and input file.
- The input and vocab files have more unigrams than bi/tri-grams.
- When we manually looked for the input terms in the HEARST Patterns, we could find more similarity between the candidate hypernyms and the gold data. 
- Hence, we have to still Normalise Hearts Patterns
==========================================================================================================================================
FUTURE PLANS:
1. Normalize HEARST patterns.
2. Applying word embeddings to the Normalized texts
3. Fetch the new results and see how the scores change

