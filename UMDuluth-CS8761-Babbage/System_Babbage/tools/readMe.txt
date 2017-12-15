This folder provied tools - the code which geenratres the new normalised text, New IS-A hearst pattern for Stage 2 of our system:

The follwoing are the files of this folder:
1. DataHIsA  - Folder which holds the IS-A Pattern "Hyponym : Hypernym" pairs extracted from the UMBC_webbase_sample corpus.
2. DataNN -  Folder which holds the new normalised texts obtainined from the UMBC_webbase_sample corpus.
3. DataNH - Folder which holds the new normalised Hearst Patterns of stage 1 (the first 6 patterns except IS-A) obtainined from the UMBC_webbase_sample corpus.
4. UMBC_webbase_sample -  Folder which conatined 5 files (out 0f 408) of UMBC_webbase_corpus of tagged text as sample data for tools in this folder.
5. Hearst_Patterns_Stage2_Norm_6.py - The python module which extacts the new normalised Hearst Patterns of folder "DataNH" (tool1)
6. Norlaization_Stage2.py -  The python file which extracts the new normalised texts in folder "DataNN" (tool2)
7. stemming -  third party tool we used to extract the stemmed(Nouns) from the input corpus in normalization step
8. 1A.english.vocabulary_1.txt - The top 20 vocabulary patterns of bi-gram and tri-gram form candidate vocabulary
9. Hearst_Pattern_Stage2_IsA.py - The python module which extacts the new IS-A Hearst Pattern of folder "DataHIsA" (tool3)
10.SampleRun.sh - The sample file used to run the tools 1 2 and 3
