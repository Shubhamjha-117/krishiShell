from sqlalchemy import func
from models.market_price import MarketPrice
from app import app
from models.market import Market
from extentions import db


with app.app_context():

    for name in ["APMC Nagpur", "APMC Pune"]:
        market = Market.query.filter_by(name=name).first()

        if market:
            market.latitude = None
            market.longitude = None
            print(f"Cleared coordinates: {market.name}")

    db.session.commit()
    
    for market in Market.query.filter(
        Market.latitude.isnot(None),
        Market.longitude.isnot(None)
    ).all():

        print(
            market.name,
            "|",
            market.latitude,
            "|",
            market.longitude
        )