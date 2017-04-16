#!flask/bin/python
from app import db, models
import json
from pprint import pprint

with open('app/static/CDA.json') as data_file:
	objects = [ i for i in json.load(data_file) ]

for i, val in enumerate(objects):
	for j, val in enumerate(objects[i]['rects']):
		record = models.CDA(image=objects[i]['image_path'],
		x1=objects[i]['rects'][j]['x1'],
		x2=objects[i]['rects'][j]['x2'],
		y1=objects[i]['rects'][j]['y1'],
		y2=objects[i]['rects'][j]['y2'])
		db.session.add(record)

db.session.commit()
