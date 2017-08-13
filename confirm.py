#!flask/bin/python
from app import db, models


cda = models.CDA.query.all()

def conflict_count(confidence):
    cda2 = models.CDA.query.filter(models.CDA.id >= 47000)
    count = 0
    for n, val in enumerate(cda2):
        if ((cda2[n].score >= confidence) and (cda2[n].GT_conflict == True)):
            count += 1
            #print("CDA ID:{}, n:{}, Conflict: {}, Confidence: {}".format(cda2[n].id,n,cda2[n].GT_conflict,cda2[n].score))
    print("There are {} instances at {} confidence".format(count,confidence))
    return count

number = 0
current_id = 0

for n, val in enumerate(cda):
    if (cda[n].GT_conflict == False):
        number += 1
        current_id = cda[n].id

print("{} instances found out of {}".format(number,current_id))

conflict_count(0.60)
conflict_count(0.50)
conflict_count(0.40)
conflict_count(0.30)
conflict_count(0.20)
conflict_count(0.10)
