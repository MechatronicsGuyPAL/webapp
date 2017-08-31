#!flask/bin/python
from app import db, models
from pprint import pprint





entries = models.Vote.query.all()

for entry in entries:
    db.session.delete(entry)
db.session.commit()

