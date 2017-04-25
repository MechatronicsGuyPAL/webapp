from app import db

class CDA(db.Model):
    __tablename__='CDA_results'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120))
    x1 = db.Column(db.SmallInteger)
    x2 = db.Column(db.SmallInteger)
    y1 = db.Column(db.SmallInteger)
    y2 = db.Column(db.SmallInteger)
    GT_conflict = db.Column(db.Boolean,default=False)
    score = db.Column(db.Float)
    votes = db.Column(db.SmallInteger,default=0)
    yes = db.Column(db.SmallInteger,default=0)
    no = db.Column(db.SmallInteger,default=0)
    unsure = db.Column(db.SmallInteger,default=0)
    result = db.Column(db.SmallInteger,default=3)
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
