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
    
    crop_id = db.column(
        db.Integer,
        db.ForeignKey("crops.id")
    )
    
    date = db.Column(
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
    
    arrival_volume = db.Column(
        db.Float
    )
    
    market = db.relationship("Market")
    crop = db.relationship("Crop")