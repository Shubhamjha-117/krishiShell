from extentions import db

class Crop(db.Model):
    __tablename__ = "crops"
    
    id = db.Column(
        db.Integer, 
        primary_key = True
    )
    
    name = db.Column(
        db.String(100),
        nullable = False
    )
    
    category = db.Column(
        db.String(100)
    )
    