# This program prints Hello, world!

import re

print 'Starting the Class Lab\n'

inputF = open("/home/manikya/Downloads/Lab1/l1.txt","r")
count = 0
endline = re.compile(r'[\.\?\!]\s+')
notEndLine = re.compile(r'(.*)(([A-Z][a-z]*\.)|(([A-Z0-9]\.)+))(.*)')
sent = re.compile(r'([\.\?\!]\s+)')
lineFront =""
lineBack = ""

for line in inputF:
    matchL = re.search(endline,line)
    # print matchL
    if matchL:
        matchNE = re.search(notEndLine,line)
        if matchNE == None:
            sens = re.split(sent,line)
            # print sens
            for sen in sens:
                print sen
                print "**"
        # else:
         # print 'END %s' % line
        print "---------------"
    else :
        print ">"

# #!/usr/bin/python
# import re
#
# line = "Cats are smarter than dogs"
#
# matchObj = re.match( r'.* are (.*?) (.*)', line, re.M|re.I)
#
# if matchObj:
#    print "matchObj.group() : ", matchObj.group()
#    print "matchObj.group(1) : ", matchObj.group(1)
#    print "matchObj.group(2) : ", matchObj.group(2)
# else:
#    print "No match!!"
