#!flask/bin/python
from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db, models

from datetime import datetime
from sqlalchemy import desc, and_
test_val_min = .2
test_val_max = .25

entries = models.CDA.query.filter(and_(models.CDA.IOU <= .25,
                                models.CDA.score >= test_val_min, 
                                test_val_max >= models.CDA.score, 
                                models.CDA.votes < 15)).order_by(models.CDA.timestamp.desc()).limit(10)
for entry in entries:
    print("entry")
