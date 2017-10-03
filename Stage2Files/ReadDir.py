import os
import json

listF = []

for file in os.listdir("/home/manikya/Downloads/newcorpus/UMBC_webbase_all/"):
    listF.append(file)


print "Lenght of list : %d" % len(listF)
setL = set(listF)
print "length of set : %d" % len(setL)
listF = sorted(listF)

print json.dumps(listF)
