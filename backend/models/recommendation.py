from extentions import db

class Recommendation(db.Model):
    __tablename__ = "recommendations"
    
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    
    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey("farmers.id")
    )
    
    crop_id = db.Column(
        db.Integer,
        db.ForeignKey("crops.id")
    )
    
    recommendation_market_id = db.Column(
        db.Integer,
        db.ForeignKey("markets.id")
    )
    
    quantity = db.Column(db.Float)
    
    net_realisation = db.Column(db.Float)
    score = db.Column(db.Float)
    
    trend = db.Column(db.String(50))
    
    farmer = db.relationship("Farmer")
    crop = db.relationship("Crop")
    market = db.relationship("Market")