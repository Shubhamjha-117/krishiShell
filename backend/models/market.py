from extentions import db

class Market(db.Model):
    __tablename__ = "markets"
    
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    
    name = db.Column(
        db.String(150),
        nullable = False
    )
    
    state = db.Column(
        db.String(100),
        nullable = False
    )
    
    district = db.Column(
        db.String(100),
        nullable = False
    )
    
    latitude = db.Column(
        db.Float
    )
    
    longitude = db.Column(
        db.Float
    )
    