import time
import nltk
import re
import json
import os

start_time = time.time()
filepath = "/home/manikya/Documents/NLP/DataH/"
ofilepath = "/home/manikya/Documents/NLP/DataH/Data1"
such_tags = re.compile(r' such/jj ')
suchas_tags = re.compile(r' such/jj as/in ')
orOther_tags = re.compile(r' or/cc other/jj ')
andOther_tags = re.compile(r' and/cc other/jj ')


for file in os.listdir(filepath):
    if "delorme.com_shu.pages_" in file:
        # cp = nltk.RegexpParser("NP: {<DT>?<JJ>*<NN>}")
        inputFN = filepath + file
        inputF = open(inputFN, 'r')
        oFile = re.sub(r'.possf2', r'_sa.txt', file)
        oFile = ofilepath + oFile
        outputFN1 = open(oFile, 'w')
        oFile = re.sub(r'.possf2', r'_sna.txt', file)
        oFile = ofilepath + oFile
        outputFN2 = open(oFile, 'w')
        oFile = re.sub(r'.possf2', r'_oo.txt', file)
        oFile = ofilepath + oFile
        outputFN3 = open(oFile, 'w')
        oFile = re.sub(r'.possf2', r'_ao.txt', file)
        oFile = ofilepath + oFile
        outputFN4 = open(oFile, 'w')
        oFile = re.sub(r'.possf2', r'_inc.txt', file)
        oFile = ofilepath + oFile
        outputFN5 = open(oFile, 'w')
        oFile = re.sub(r'.possf2', r'_esp.txt', file)
        oFile = ofilepath + oFile
        outputFN6 = open(oFile, 'w')
        brown = nltk.corpus.brown
        for line in inputF:
            line = line.lower()
            line = re.sub(r'(\S+)_(\S+)', r'\1/\2', line)
            matchsuch = re.search(such_tags, line)
            matchsuchas = re.search(suchas_tags, line)
            matchorOther = re.search(orOther_tags, line)
            matchAndOther = re.search(andOther_tags, line)
            if matchsuch:
                # OLD CODE
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))?'
                # OLD CODE
                np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *)+'
                # OLD CODE
                lsep = '(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+'

                if matchsuchas:
                    # np = '(?:,/,)?'
                    # np = '(?:\S+/dt[a-z]* )?(?:\S+/jj[a-z]*)* *(?:\S+/nn[a-z]*)* *(?:(?:(?:,/,)|(?:and|or)/cc))?'
                    # np = '(?:\S+/dt[a-z]*)? *(?:\S+/jj[a-z]*)* *(?:\S+/nn[a-z]*)+ *(?:(?:(?:,/,)|(?:and|or)/cc))?'

                    #OLD CODE
                    # np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))?'
                    #NEW CODE
                    # np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+'

                    # np2 ='(?:(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *)+'

                    #OLD CODE
                    # np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *)+'
                    #NEW CODE
                    # np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+(?:,/,)? *)+'

                    #NEW CODE
                    cc = '(?:(?:and)|(?:or))'

                    # np2 = (?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))?
                    # lsep = '(?:(?:(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc))? *)'

                    #OLD CODE
                    # lsep = '(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+'
                    #NEW CODE
                    # lsep = '(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+'

                    # np2 = '(?:(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+)'
                    # sep = '(?:(?:(?:,/,)|(?:(?:and)|(?:or))/cc))? *'
                    # np = ",/,"
                    # pattern = re.compile(r'(?:,/,)? such/jj as/in ') IMP
                    # pattern = re.compile(r'%s such/jj as/in (?:%s %s?)+' % (np, np2, sep))

                    #OLD CODE
                    pattern = re.compile(r'%s such/jj as/in (?:%s )?%s' % (np, np2, lsep))

                    #new code
                    # pattern = re.compile(r'%s (?:,/, )?such/jj as/in (?:%s )?(?:%s )?%s' % (np, np2, cc, np))

                    # pattern = re.compile(r'%s such/jj as/in ' % (np))
                    # pattern = r',/,? such/jj as/in'
                    # pattern = re.compile(r'(,/,)? such/jj as/in ')
                    # print "===================================="
                    # print line
                    # line1 = re.findall(r'(\S+/DT[A-Z]* ?)(\S+/JJ[A-Z]* )*(\S+/NN[A-Z]*)  ', )
                    npTuple = re.findall(pattern, line, flags=0)
                    for item in npTuple:
                        item = re.sub(r'(\S+)/(\S+)', r'\1', item)
                        # print item
                        outputFN1.write('%s \n' % item)
                else:
                    # print "==================================="
                    pattern = re.compile(r' such/jj %s as/in (?:%s )?%s' % (np, np2, lsep))
                    npTuple = re.findall(pattern, line, flags=0)
                    for item in npTuple:
                        item = re.sub(r'(\S+)/(\S+)', r'\1', item)
                        # print item
                        outputFN2.write('%s \n' % item)
            elif matchorOther:
                # OLD CODE
                np = '(?:\S+/dt[a-z]* *)?(?:\S+/jj[a-z]* *)*(?:\S+/nn[a-z]* *)+'
                # OLD CODE
                np2 = '(?:(?:,/,) *(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+)'
                # OLD CODE
                # lsep = '(?:(?:,/,)? ?(?:(?:and)|(?:or))/cc *)?(?:\S+/dt[a-z]* *)?(?:\S+/(?:(?:jj[a-z]*)|(?:vb[ng])) *)*(?:\S+/nn[a-z]* *)+'
                # , or|and Other
                oao = '(?:,/, )?(?:(?:and)|(?:or))_cc other_jj '
                pattern = re.compile(r' %s(?:%s)* ?%s ?%s' % (np,np2,oao,np))
                npTuple = re.findall(pattern, line, flags=0)
                for item in npTuple:
                    item = re.sub(r'(\S+)/(\S+)', r'\1', item)
                    print item
                    # outputFN2.write('%s \n' % item)

                #
                # print "------------------"



outputFN1.close()
outputFN2.close()
outputFN3.close()
outputFN4.close()
outputFN5.close()
outputFN6.close()


print "The EXECUTION TIME is : %s" % (time.time() - start_time)