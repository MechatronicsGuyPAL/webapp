#!flask/bin/python
from app import db, models
from pprint import pprint





votes = models.Vote.query.all()

for i, val in enumerate(votes):
    print("number: {}, Crater: {}, result: {}".format(votes[i].id, votes[i].crater_id, votes[i].vote_result))

