from services.market_service import get_latest_prices_for_crop
from models.crop import Crop
from app import app

with app.app_context():
    crop = Crop.query.first()

    prices = get_latest_prices_for_crop(crop.id)

    len(prices)

    for p in prices[:5]:
        print(
            p.market.name,
            p.crop.name,
            p.arrival_date,
            p.modal_price
        )