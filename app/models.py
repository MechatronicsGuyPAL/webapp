from app import db

class CDA(db.Model):
    __tablename__='CDA_results'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    x1 = db.Column(db.SmallInteger)
    x2 = db.Column(db.SmallInteger)
    y1 = db.Column(db.SmallInteger)
    y2 = db.Column(db.SmallInteger)
    score = db.Column(db.Float)
    GT_conflict = db.Column(db.Boolean,default=True)
    votes = db.Column(db.SmallInteger,default=0)
    timestamp = db.Column(db.DateTime)

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


class Training(db.Model):
    __tablename__='training_entries'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    x1 = db.Column(db.SmallInteger)
    x2 = db.Column(db.SmallInteger)
    y1 = db.Column(db.SmallInteger)
    y2 = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<Training %r>' % self.id

class Vote(db.Model):
    __tablename__='votes'
    id = db.Column(db.Integer, primary_key=True)
    crater_id = db.Column(db.Integer, db.ForeignKey('CDA_results.id'))
    start_timestamp = db.Column(db.DateTime)
    end_timestamp = db.Column(db.DateTime)
    vote_result = db.Column(db.String(1))
    x1_new = db.Column(db.SmallInteger, nullable =True)
    x2_new = db.Column(db.SmallInteger, nullable =True)
    y1_new = db.Column(db.SmallInteger, nullable =True)
    y2_new = db.Column(db.SmallInteger, nullable =True)
    session_data = db.Column(db.String(120))    

    def __repr__(self):
        return '<Vote %r>' % self.id


