from app import db
#var1 field in CDA is used to hold the result of the vote process, [yes,no,unsure,borderline,review,recenter]
#var2 field in CDA is used in 'recenter' results to hold the ID of the corresponding vote with the best recenter coordinates
#var2 is empty for entries not labeled 'recenter'
class CDA(db.Model):
    __tablename__='CDA_results'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    x1 = db.Column(db.SmallInteger)
    x2 = db.Column(db.SmallInteger)
    y1 = db.Column(db.SmallInteger)
    y2 = db.Column(db.SmallInteger)
    score = db.Column(db.Float)
    GT_conflict = db.Column(db.Boolean)
    votes = db.Column(db.SmallInteger,default=0)
    timestamp = db.Column(db.DateTime)
    IOU = db.Column(db.Float)
    var1 = db.Column(db.String(120))
    var2 = db.Column(db.String(120))

    def __repr__(self):
        return '<CDA %r>' % self.id



class GroundTruth(db.Model):
    __tablename__='groundtruths'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    x1 = db.Column(db.SmallInteger)
    x2 = db.Column(db.SmallInteger)
    y1 = db.Column(db.SmallInteger)
    y2 = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<GroundTruth %r>' % self.id

#var1 in Vote is used to hold the  combined z-score of the xy recenter coordinates for recenter finished craters
#var2 will hold the identifier 'super_user_vote' to identify a super user vote on a crater. A single vote by a super user will 
#immediately update the crater entry result field so that crater will not need 15 user votes. 

class Vote(db.Model):
    __tablename__='votes'
    id = db.Column(db.Integer, primary_key=True)
    crater_id = db.Column(db.Integer, db.ForeignKey('CDA_results.id'))
    start_timestamp = db.Column(db.DateTime)
    end_timestamp = db.Column(db.DateTime)
    vote_result = db.Column(db.String(20))
    x1_new = db.Column(db.SmallInteger, nullable =True)
    x2_new = db.Column(db.SmallInteger, nullable =True)
    y1_new = db.Column(db.SmallInteger, nullable =True)
    y2_new = db.Column(db.SmallInteger, nullable =True)
    session_data = db.Column(db.String(120))
    var1 = db.Column(db.String(120))
    var2 = db.Column(db.String(120))    

    def __repr__(self):
        return '<Vote %r>' % self.id


