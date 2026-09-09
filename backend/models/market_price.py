from extentions import db

class MarketPrice(db.Model):
    __tablename__ = "market_price"
    
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    
    market_id = db.Column(
        db.Integer,
        db.ForeignKey("markets.id"),
        nullable = False
    )
    
    crop_id = db.Column(
        db.Integer,
        db.ForeignKey("crops.id"),
        nullable=False
    )
    
    variety = db.Column(
        db.String(150)
    )
    
    grade = db.Column(
        db.String(100)
    )
    
    arrival_date = db.Column(
        db.Date,
        nullable = False
    )
    
    min_price = db.Column(
        db.Float
    )
    
    max_price = db.Column(
        db.Float
    )
    
    modal_price = db.Column(
        db.Float
    )
    
    market = db.relationship("Market")
    crop = db.relationship("Crop")