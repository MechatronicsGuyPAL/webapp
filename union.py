#!flask/bin/python
from app import db, models

from pprint import pprint
from datetime import datetime


GT = models.GroundTruth.query.all()
print("GT has {} entries").format(len(GT))
cda = models.CDA.query.all()
cda_len = len(cda)
print("CDA has {} entries").format(cda_len)

IOU_count = 0



def bb_intersection_over_union(cda, GT):
    iou = 0

    # determine the (x, y)-coordinates of the intersection rectangle
    xA = int(max(cda.x1, GT.x1))
    yA = int(max(cda.y1, GT.y1))
    xB = int(min(cda.x2, GT.x2))
    yB = int(min(cda.y2, GT.y2))

   
   # check that the two boxes have overlapping area
    if ((xA <= xB) and (yA <= yB)):
        #check that the boxes are similar sizes
        size_ratio = (cda.x2-cda.x1) / float(GT.x2-GT.x1)
        if ((size_ratio >= 0.25) and (size_ratio <= 4)):
            # compute the area of intersection rectangle
            interArea = (xB - xA + 1) * (yB - yA + 1)
            # compute the area of both the prediction and ground-truth
            # rectangles
            boxAArea = (int(cda.x2) - int(cda.x1) + 1) * (int(cda.y2) - int(cda.y1) + 1)
            boxBArea = (int(GT.x2) - int(GT.x1) + 1) * (int(GT.y2) - int(GT.y1) + 1)

            # compute the intersection over union by taking the intersection
            # area and dividing it by the sum of prediction + ground-truth
            # areas - the interesection area
            iou = interArea / float(boxAArea + boxBArea - interArea)

            #print("IA:{}, A:{}, B:{}".format(interArea, boxAArea, boxBArea))

    # return the intersection over union value
    return iou

def conflict_count(confidence):
    cda2 = models.CDA.query.all()
    count = 0
    for n, val in enumerate(cda2):
        if ((cda2[n].score >= confidence) and (cda2[n].GT_conflict == True)):
            count += 1
            #print("CDA ID:{}, n:{}, Conflict: {}, Confidence: {}".format(cda2[n].id,n,cda2[n].GT_conflict,cda2[n].score))
    print("There are {} instances at {} confidence".format(count,confidence))
    return count


for n, val in enumerate(cda):
    print("Currently on CDA record #{} out of {}".format(n,cda_len))
    for m, val in enumerate(GT):
        #check that boxes are for the same image
        if ((cda[n].image == GT[m].image) and (cda[n].id >= 47700)):
            iou = bb_intersection_over_union(cda[n], GT[m])
            if iou >= 0.5:
                IOU_count += 1
                cda[n].GT_conflict = False
                #print("CDA ID:{}, n:{} - x1:{}, y1:{}, x2:{}, y2:{}, Conflict: {}".format(cda[n].id,n,cda[n].x1,cda[n].y1,cda[n].x2,cda[n].y2,cda[n].GT_conflict))            
                #print("CDA ID:{}, n:{} - x1:{}, y1:{}, x2:{}, y2:{}, Conflict: {}".format(cda[n].id,n,cda[n].x1,cda[n].y1,cda[n].x2,cda[n].y2,cda[n].GT_conflict))
                #print("GT ID:{}, m:{} - x1:{}, y1:{}, x2:{}, y2:{}".format(GT[m].id,m,GT[m].x1,GT[m].y1,GT[m].x2,GT[m].y2))
                #print("IOU- {:.4f}".format(iou))
                #print("IOU Count: {}".format(IOU_count))
                db.session.add(cda[n])
                db.session.commit()
                break

print("IOU Count: {}".format(IOU_count))
conflict_count(0.60)
conflict_count(0.50)
conflict_count(0.40)
conflict_count(0.30)
conflict_count(0.20)
conflict_count(0.10)
