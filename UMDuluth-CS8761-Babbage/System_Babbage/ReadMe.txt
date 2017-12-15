Author: Swathi

The folder contains the following:
1. Data: folder with stage1-trial and training results alog with input data + the SemEval task zip
2. Output : forler to store the results of various modules , sample results and the main results
3. src : System_Babbge source code which we have written
4. Third-party-Tools: Some thirm party tools for GloVe and ans some other projects.
5. tools : Directory which has TOOLs to generate HEARSTS PATTERN (IS-A : NP1 is(a|an|the) NP0), Generate NEW NORMLAIZED DATA, NORMALIZED HEARTS PATTERNS and Tool to generate word embeddings.
6. SampleResults.txt: This is sample results of System_Babbage's final merged outputs [9-Complete results, 10- Concepts, 11-Entities]
7. runIt.sh - THE MAIN FILE to start execution as "sh runIt.sh" - as a sudo user.
8. Swathi_stage2_report(.odt|.txt) : explanantion about System_Babbage, What module we have how did we derive to thpose modules, what different decicitions did we make to generate the final decision, etc. [.txt version is made to make it readable in akk/ukko]
9. results_<folder_name>_timestamp : the results file with just the System_Babbage results. where <folder_name> is the name given to store the outpus in putput folder. It is store in $OUTPUS_DIR in runIt.sh.

