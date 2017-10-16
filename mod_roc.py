#!flask/bin/python
from app import db, models

#This module is intended to create a dataset for graphing ROC curves
#(Recieiver Operating Charactersitc). The resultant CSV files will be
#saved in the webapp/data/csvs diretory.


#insert values for desired Intersection Over Union percentage. 
#Each value will produce a dataset for graphing an ROC curve.
#each value should be greater than 0 and less than 1.
IOU_threshold_list = [0.2, 0.25, 0.3, 0.35]

#Insert the number of data points you want.
number_data_points = 100

#Use this variable to consider the evaluated results
#set to True to use the results, set to False to ignore the results
use_evaluated_results = False




#*************************************************
#       This code should not be altered
#************************************************* 

#set extreemely large minimum pixle count so it is immediately replaced
min_pix = 5000
num_small = 0




GT = models.GroundTruth.query.all()
gt_len = len(GT)
print("GT has {} entries").format(gt_len)
cda = models.CDA.query.all()
cda_len = len(cda)
print("CDA has {} entries").format(cda_len)


#TP_original = number of predictions where (IOU >= IOU_threshold) and (score >= confidence)
#TP_evaluated = original + predictions where (IOU < IOU_threshold) and vote result is 'yes' or 'recenter'
def TPR(gt_len, cda, confidence, IOU_threshold, use_results):
    TP_original = 0
    TP_evaluated = 0
    TP = 0
    for n, val in enumerate(cda):
        if (cda[n].IOU >= IOU_threshold):
            if (cda[n].score >= float(confidence)):
                TP_original += 1
        if (cda[n].IOU < IOU_threshold):
            if (cda[n].score >= float(confidence)):
                if ((cda[n].vote_result == 'yes') or (cda[n].vote_result == 'recenter')): 
                    TP_evaluated += 1
        if use_results == True:
            TP = TP_original + TP_evaluated
        else:
            TP = TP_original
    tpr = (float(TP)/float(gt_len))
    return tpr

#FP_original = number predictions where (score >= confidence) and (IOU < IOU_threshold) and (crater is not small)
#FP_evaluated = same as original - any craters where (vote result = 'yes' or 'recenter')
#Total predictions = number of predictions at confidence, minus small predictions at confidence
def FPR(cda, confidence, IOU_threshold, use_results):
    FP_original = 0
    FP_evaluated = 0
    FP = 0
    num_small = 0
    predictions = 0
    for n, val in enumerate(cda):
        if (cda[n].score >= confidence):
            predictions += 1
            if (cda[n].var1 == "small"):
                num_small += 1
            if ((cda[n].IOU < IOU_threshold) and (cda[n].var1 != "small")):
                FP_original += 1
                if ((cda[n].vote_result == 'yes') or (cda[n].vote_result == 'recenter')): 
                    FP_evaluated +=1
    tot_pred = predictions - num_small
    if use_results == True:
        FP = FP_original - FP_evaluated
    else:
        FP = FP_original

    fpr = (float(FP)/float(tot_pred))
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
        if cda[n].var1 != "small":
            cda[n].var1 = "small"
            db.session.add(cda[n])
        num_small += 1
print("{} total small craters found.".format(num_small))
db.session.commit()


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


step_size = 1.0/float(number_data_points)
IOU_threshold = .35

if use_evaluated_results == True:
    name_string = '_evaluated_'
else:
    name_string = '_original_'
IOU_string = str(int(IOU_threshold*100.0))
file_name_path = 'data/csvs/ROC'+name_string+IOU_string

f_ROC = open(file_name_path,'w')
f_ROC.write('Confidence,TPR,FPR\n')

for confidence in my_range(0, 1, step_size):
    tpr = TPR(gt_len, cda, confidence, IOU_threshold, use_evaluated_results)
    fpr = FPR(cda, confidence, IOU_threshold, use_evaluated_results)
    print("Confidence, {}, TPR, {}, FPR, {}, end/n".format(confidence, tpr, fpr))
    f_ROC.write("{},{},{}\n".format(confidence,tpr,fpr))
f_ROC.close()
            
# GT has 31132 entries
# CDA has 82903 entries

# minimum pixels for GT entries is 12
# small CDA entries found: 3141
