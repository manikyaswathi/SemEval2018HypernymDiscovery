import gensim, logging
import os
import re
import sys
from nltk import PorterStemmer

# @AUTHOR: MANIKYA SWATHI VALLABHAJOSYULA
# PURPOSE : To Create word embeddings 
# Run : python Create_word2vec_embedding.py input_folder embedding_name

# THis is used for create the word embedding - CBOW ; SG

# REFERENCE : https://radimrehurek.com/gensim/apiref.html
# The following API's are used to create word embeddings

# read the input sentences
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                line = re.sub(r'(\S+)_\S+', r'\1', line)
                yield line.split()

corpus = sys.argv[1]                    # input_folder
filename = sys.argv[2]                  # output_file
sentences = MySentences(corpus)

CBOW_model = 1                          # set this to 1 for CBOW model, set to 0 for Skip-gram 

if CBOW_model:
    '''
    CONFIGURATION FILE:
        Dimentions = 300
        window size = 20
        minimum frequency = 10
        Model = CBOW
    '''
    model = gensim.models.word2vec.Word2Vec(sentences, size=300, window=20, min_count=10, sample=1e-5, workers=20, iter=1)
    model.save(filename)
else:
    '''
    CONFIGURATION FILE:
        Dimentions = 300
        window size = 20
        minimum frequency = 10
        Model = Skip-Gram
    '''
    model = gensim.models.word2vec.Word2Vec(sentences, size=300, window=20, min_count=10, sample=1e-5, workers=20, sg=1, hs=0, negative=5, iter=1)
    model.save(filename)
    

''' Word2Vec Model configurations
gensim.models.word2vec.Word2Vec(sentences=None, size=100, alpha=0.025, window=5, 
min_count=5, max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, 
sg=0, hs=0, negative=5, cbow_mean=1, hashfxn=<built-in function hash>, iter=5, 
null_word=0, trim_rule=None, sorted_vocab=1, batch_words=10000, compute_loss=False)

'''
