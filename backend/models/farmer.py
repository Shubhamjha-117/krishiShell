from extentions import db

class Farmer(db.Model):
    __tablename__ = "farmers"
    
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    
    name = db.Column(
        db.String(150),
        nullable = False
    )
    
    phone = db.Column(
        db.String(20)
    )
    
    location = db.Column(
        db.String(150)
    )
    
    latitude = db.Column(
        db.Float
    )
    
    longitude = db.Column(
        db.Float
    )