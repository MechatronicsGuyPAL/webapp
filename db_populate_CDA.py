#!flask/bin/python
from app import db, models
import json
from pprint import pprint
from datetime import datetime

#Delete old CDA entries before importing new data
entries = models.CDA.query.all()
for entry in entries:
    db.session.delete(entry)

db.session.commit()

#Open CDA file and populate the CDA database table
with open('app/static/CDA.json') as data_file:
        objects = [ i for i in json.load(data_file) ]

for i, val in enumerate(objects):
        for j, val in enumerate(objects[i]['rects']):
                record = models.CDA(image=objects[i]['image_path'],
                x1 = objects[i]['rects'][j]['x1'],
                x2 = objects[i]['rects'][j]['x2'],
                y1 = objects[i]['rects'][j]['y1'],
                y2 = objects[i]['rects'][j]['y2'],
                score = objects[i]['rects'][j]['score'],
                timestamp = datetime.utcnow())
                db.session.add(record)

db.session.commit()



#Delete old database entries before importing new data
entries = models.GroundTruth.query.all()
for entry in entries:
    db.session.delete(entry)

db.session.commit()

#Open CDA file and populate the CDA database table
with open('app/static/groundtruth.json') as data_file:
        objects = [ i for i in json.load(data_file) ]

for i, val in enumerate(objects):
        for j, val in enumerate(objects[i]['rects']):
                record = models.GroundTruth(image=objects[i]['image_path'],
                x1 = objects[i]['rects'][j]['x1'],
                x2 = objects[i]['rects'][j]['x2'],
                y1 = objects[i]['rects'][j]['y1'],
                y2 = objects[i]['rects'][j]['y2'])
                db.session.add(record)

db.session.commit()

