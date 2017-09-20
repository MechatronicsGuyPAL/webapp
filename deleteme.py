#!flask/bin/python
from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db, models
from models import CDA
from datetime import datetime
from sqlalchemy import desc, and_

entries = models.CDA.query.filter(and_(CDA.IOU <= .25,
                                CDA.score >= test_val_min, 
                                CDA.score <= test_val_max, 
                                CDA.votes < 15)).order_by(CDA.timestamp.desc()).limit(1).first()
