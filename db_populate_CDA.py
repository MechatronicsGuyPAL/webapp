#!flask/bin/python
from app import db, models
import json
from pprint import pprint
from datetime import datetime

#Delete old CDA entries before importing new data
entries = models.CDA.query.all()
n=0
for entry in entries:
    db.session.delete(entry)
    n+=1
    if (n >= 500):
        db.session.commit()
        n=0
        print("commit")
db.session.commit()


#Open CDA file and populate the CDA database table
with open('data/jsons/webapp_data_V2.json') as data_file:
        objects = [ i for i in json.load(data_file) ]

for i, val in enumerate(objects):
        for j, val in enumerate(objects[i]['rects']):

                record = models.CDA(image=objects[i]['image_path'],
                x1 = objects[i]['rects'][j]['x1'],
                x2 = objects[i]['rects'][j]['x2'],
                y1 = objects[i]['rects'][j]['y1'],
                y2 = objects[i]['rects'][j]['y2'],
                score = objects[i]['rects'][j]['score'],
                timestamp = datetime.utcnow(),
                GT_conflict = objects[i]['rects'][j]['GT_conflict'],
                IOU = objects[i]['rects'][j]['IOU'],
                var1 = "empty",
                var2 = "empty")

                db.session.add(record)
        print("commit")
        db.session.commit()
db.session.commit()
print("CDA populated")

# #Delete old database entries before importing new data
# entries = models.GroundTruth.query.all()
# n=0
# for entry in entries:
#     db.session.delete(entry)
#     n+=1
#     if (n >= 500):
#         db.session.commit()
#         n=0
#         print("commit")
# db.session.commit()

# print("clear Ground Truth, begin populate GT")

# #Open CDA file and populate the CDA database table
# with open('data/jsons/groundtruth_full.json') as data_file:
#         objects = [ i for i in json.load(data_file) ]

# for i, val in enumerate(objects):
#         for j, val in enumerate(objects[i]['rects']):
#                 record = models.GroundTruth(image=objects[i]['image_path'],
#                 x1 = objects[i]['rects'][j]['x1'],
#                 x2 = objects[i]['rects'][j]['x2'],
#                 y1 = objects[i]['rects'][j]['y1'],
#                 y2 = objects[i]['rects'][j]['y2'])
#                 db.session.add(record)
#         print("commit")
#         db.session.commit()
# db.session.commit()

# print("finished populate GT")


