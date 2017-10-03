import time
import nltk
import re
import json

start_time = time.time()

# for file in os.listdir("/home/manikya/Documents/NLP/Data/"):
#     if "delorme.com_shu.pages_" in file:
#         inputFN = "/home/manikya/Documents/NLP/Data/" + file
#         inputF = open(inputFN, 'r')
#         outputFN = re.sub(r'.possf2', r'.txt', file)
#         oFile = "/home/manikya/Documents/NLP/Data/" + outputFN
#         outputF = open(oFile, 'w')
#         for line in inputF:
#             Flist = []
#             line = re.sub(r'(\S+)_(\S+)', r'\1', line)
#             line = line.lower()
#             unLine = line
#             outputF.write(line)


#
# text = '''
# The titular threat of The Blob has always struck me as the ultimate movie
# monster: an insatiably hungry, amoeba-like mass able to penetrate
# virtually any safeguard, capable of--as a doomed doctor chillingly
# describes it--"assimilating flesh on contact.
# Snide comparisons to gelatin be damned, it's a concept with the most
# devastating of potential consequences, not unlike the grey goo scenario
# proposed by technological theorists fearful of
# artificial intelligence run rampant.
# '''
#
# blob = TextBlob(text)
# tagsL = blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
#                     #  ('threat', 'NN'), ('of', 'IN'), ...]
#
# NPList = blob.noun_phrases   # WordList(['titular threat', 'blob',
#                     #            'ultimate movie monster',
#                     #            'amoeba-like mass', ...])
#
# print json.dumps(tagsL)
#
# print json.dumps(NPList)

# inputFN = "/home/manikya/Documents/NLP/Data/" + "Sample.possf2"
# inputF = open(inputFN, 'r')
# outputFN = re.sub(r'.possf2', r'.txt', file)
# oFile = "/home/manikya/Documents/NLP/Data/" + outputFN
# outputF = open(oFile, 'w')
# for line in inputF:
#     line = re.sub(r'(\S+)_(\S+)', r'\1', line)
#     line = line.lower()
#     unLine = line
#     outputF.write(line)

cp = nltk.RegexpParser("NP: {<DT>?<JJ>*<NN>}")
# brown = nltk.corpus.brown
inputFN = "/home/manikya/Documents/NLP/Data/" + "Sample.possf2"
inputF = open(inputFN, 'r')
# outputFN = re.sub(r'.possf2', r'.txt', file)
oFile = "/home/manikya/Documents/NLP/Data/Sample7.txt"
outputFN = open(oFile, 'w')
# cp = nltk.RegexpParser('CHUNK: {<V.*> <TO> <V.*>}')
brown = nltk.corpus.brown
# for sent in brown.tagged_sents():
for line in inputF:
    # print line
    line = line.lower()
    # print "===================================="
    # print line
    line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
    # np = '(?:,/,)?'
    # np = '(?:\S+/dt[a-z]* )?(?:\S+/jj[a-z]*)* *(?:\S+/nn[a-z]*)* *(?:(?:(?:,/,)|(?:and|or)/cc))?'
    # np = '(?:\S+/dt[a-z]*)? *(?:\S+/jj[a-z]*)* *(?:\S+/nn[a-z]*)+ *(?:(?:(?:,/,)|(?:and|or)/cc))?'
    np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))?'

    # np2 ='(?:(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *)+'

    np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *)+'
    # np2 = (?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))?

    # lsep = '(?:(?:(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc))? *)'
    lsep = '(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+'


    # np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+)'
    # sep = '(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *'

    # np = ",/,"
    # pattern = re.compile(r'(?:,/,)? such/jj as/in ') IMP

    # pattern = re.compile(r'%s such/jj as/in (?:%s %s?)+' % (np, np2, sep))
    pattern = re.compile(r'%s such/jj as/in (?:%s )?%s' % (np, np2, lsep))

    # pattern = re.compile(r'%s such/jj as/in ' % (np))


    # pattern = r',/,? such/jj as/in'
    # pattern = re.compile(r'(,/,)? such/jj as/in ')
    # print "===================================="
    # print line
    # line1 = re.findall(r'(\S+/DT[A-Z]* ?)(\S+/JJ[A-Z]* )*(\S+/NN[A-Z]*)  ', )
    npTuple = re.findall(pattern, line, flags=0)
    for item in npTuple:
        item = re.sub(r'(\S+)/(\S+)', r'\1', item)
        # print type(item)
        outputFN.write('%s \n' % item)
    # npTuple = re.match(pattern, line)
    # print json.dumps(npTuple)
    # print npTuple
    # npList = list(nltk.chain(*npTuple))
    # print json.dumps(npList)
    print "------------------"
    # tree = cp.parse(sent)
    # for subtree in tree.subtrees():
    #     if subtree.label() == 'CHUNK':
    #         print(subtree)



print "The EXECUTION TIME is : %s" % (time.time() - start_time)