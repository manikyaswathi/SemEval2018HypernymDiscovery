AUTHOR : MANIKYA SWATHI VALLABHAJOSYULA

The following are the files in this folder:
1. 1A.english.training.data.txt : The input training words (1500)
2. 1A.english.trial.data.txt : The input trial words (50)
3. 1A.english.vocabulary.txt : The candidate vocabulary 
4. UMBCCEIS.txt : The IS-A patterns - 2633421 pairs obtains from NP1 is (a|an|the) NP0 from UMBC Corpus (Download From Google Drive https://drive.google.com/open?id=1fa8KVY2QmiRwAwQZdxEsDCBFNoNejl2b the file and place it here.) 
5. Stage2Model1IsA.py : The main module which finds Part-Of + IS-A patterns
6. prepareNew.sh : The shell scipt which reals the length of input file and based on it creats parallel folder structure to execute the Stage2Model1IsA.py program. (this reduces the run time from 18+ hours to 1:30 hours.
7. Sample_Model1.LOG : This is the sample log file created by the shell script
8. stemming : The thordparty module copy tp do stemming of output hypernyms.
9. UMBCCEIS_top_bottom_1000.txt : The IS-A patterns - top 1000 and bottom 1000 pairs from UMBCCEIS.txt(https://drive.google.com/open?id=1fa8KVY2QmiRwAwQZdxEsDCBFNoNejl2b) file as a sample.
