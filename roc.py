#!flask/bin/python
from app import db, models


min_pix = 5000
num_small = 0
num_big = 0



GT = models.GroundTruth.query.all()
gt_len = len(GT)
print("GT has {} entries").format(gt_len)
cda = models.CDA.query.all()
cda_len = len(cda)
print("CDA has {} entries").format(cda_len)

#TP = number of predictions where (conflict = false) and (score >= confidence)
def TPR(gt_len, cda, confidence):
    TP = 0
    for n, val in enumerate(cda):
        if (cda[n].GT_conflict == False):
            if (cda[n].score >= float(confidence)):
                TP += 1
    tpr = (float(TP)/float(gt_len))
    print("TPR - TP/GT = {}/{}".format(TP,gt_len))
    return tpr

#FP = number predictions where (score >= confidence) and (conflict = True) and (crater is not small)
#Total predictions = number of predictions at confidence, minus small predictions at confidence
def FPR(cda, confidence):
    FP = 0
    num_small = 0
    predictions = 0
    for n, val in enumerate(cda):
        if (cda[n].score >= confidence):
            predictions += 1
            if (cda[n].var1 == "small"):
                num_small += 1
            if ((cda[n].GT_conflict == True) and (cda[n].var1 != "small")):
                FP += 1
    tot_pred = predictions - num_small

    fpr = (float(FP)/float(tot_pred))
    print("FPR - FP/Predictions = {}/{}".format(FP,tot_pred))
    return fpr

            



print("Checking for minimum GT size")
for m, val in enumerate(GT):
    pix_x = GT[m].x2 - GT[m].x1
    pix_y = GT[m].y2 - GT[m].y1
    if min_pix > pix_x:
        min_pix = pix_x
        print("minimum pixels is {}, GT record number {}, {}".format(min_pix, GT[m].id, GT[m].image))
    if min_pix > pix_y:
        min_pix = pix_y
        print("minimum pixels is {}, GT record number {}, {}".format(min_pix, GT[m].id, GT[m].image))

print("Checking for small craters")
for n, val in enumerate(cda):
    cda_pix_x = cda[n].x2-cda[n].x1
    cda_pix_y = cda[n].y2-cda[n].y1
    #set votes to a large number to identify small conflicts
    if ((cda_pix_x < min_pix) or (cda_pix_y < min_pix)):
        cda[n].var1 = "small"
        db.session.add(cda[n])
        num_small += 1
print("Small craters found, {} total.".format(num_small))
db.session.commit()
num_big = cda_len - num_small

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

for x in my_range(0, 1, .1):
    tpr = TPR(gt_len, cda, x)
    fpr = FPR(cda, x)
    print("Confidence: TPR: FPR: -- {} : {} : {}".format(x, tpr, fpr))
            
# GT has 31132 entries
# CDA has 82903 entries

# minimum pixels for GT entries is 12
# small CDA entries found: 3141
