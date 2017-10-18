#!flask/bin/python
from app import db, models
from sqlalchemy import and_
import better_exceptions


entries = models.CDA.query.filter(and_(models.CDA.vote_result != None, models.CDA.results_SU_vote >= 1)).order_by(models.CDA.score.desc())
for i, val in enumerate(entries):
    print("{}: Confidence {}".format(i+1,entries[i].score))



    votes = models.Vote.query.filter(and_(models.Vote.crater_id == entries[i].id, models.Vote.vote_type == "super_user_vote"))
    for x, val in enumerate(votes):
        print("vote {}".format(x+1))
#     for vote in votes:
#         db.session.delete(vote)


# for entry in entries:
#     entry.vote_result = None
#     entry.results_SU_vote = None
#     db.session.add(entry)


# print('Committing changes')
# db.session.commit()

