#!flask/bin/python
from app import db, models




cda = models.CDA.query.all()

unions = 0
conflicts = 0
count001 = 0
count005 = 0
count01 = 0
count02 = 0
count03 = 0
count04 = 0
count05 = 0
count06 = 0
count07 = 0
countGT01 = 0

for n, val in enumerate(cda):
    score = cda[n].score
    if (cda[n].GT_conflict == False):
        unions += 1
    else:
        conflicts += 1
        if ((score >= 0.01)):
            countGT01 += 1
            count001 += 1
            if ((score >= 0.05)):
                count005 += 1
                count001 -= 1
                if ((score >= 0.1)):
                    count01 += 1
                    count005 -= 1
                    if ((score >= 0.2)):
                        count02 += 1
                        count01 -= 1
                        if ((score >= 0.3)):
                            count03 += 1
                            count02 -= 1
                            if ((score >= 0.4)):
                                count04 += 1
                                count03 -= 1
                                if ((score >= 0.5)):
                                    count05 += 1
                                    count04 -= 1
                                    if ((score >= 0.6)):
                                        count06 += 1
                                        count05 -= 1
                                        if ((score >= 0.7)):
                                            count07 += 1
                                            count06 -= 1



count0 = conflicts - countGT01

print("Unions : {}, Conflicts: {}".format(unions, conflicts))
print("x > 0.70 confidence: {} conflicts".format(count07))
print("0.70 > x > 0.60 confidence: {} conflicts".format(count06))
print("0.60 > x > 0.50 confidence: {} conflicts".format(count05))
print("0.50 > x > 0.40 confidence: {} conflicts".format(count04))
print("0.40 > x > 0.30 confidence: {} conflicts".format(count03))
print("0.30 > x > 0.20 confidence: {} conflicts".format(count02))
print("0.20 > x > 0.10 confidence: {} conflicts".format(count01))
print("0.10 > x > 0.05 confidence: {} conflicts".format(count005))
print("0.05 > x > 0.01 confidence: {} conflicts".format(count001))
print("x < 0.01 confidence: {} conflicts".format(count0))
