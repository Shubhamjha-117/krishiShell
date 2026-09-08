import os
import requests
from datetime import datetime

from app import app
from extentions import db

from models.crop import Crop
from models.market import Market
from models.market_price import MarketPrice


API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

API_KEY = os.getenv("DATA_GOV_API_KEY")


def fetch_market_data():
    params = {
        "api-key": API_KEY,
        "format": "json",
        "offset": 0,
        "limit": 10
    }

    response = requests.get(
        API_URL,
        params=params,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()


def get_or_create_crop(crop_name):
    crop = Crop.query.filter_by(
        name=crop_name
    ).first()

    if crop:
        return crop

    crop = Crop(
        name=crop_name
    )

    db.session.add(crop)
    db.session.flush()

    return crop


def get_or_create_market(state, district, market_name):
    market = Market.query.filter_by(
        name=market_name,
        state=state,
        district=district
    ).first()

    if market:
        return market

    market = Market(
        name=market_name,
        state=state,
        district=district
    )

    db.session.add(market)
    db.session.flush()

    return market


def parse_date(date_string):
    return datetime.strptime(
        date_string,
        "%d/%m/%Y"
    ).date()


def save_record(record):
    state = record.get("state")
    district = record.get("district")
    market_name = record.get("market")

    commodity = record.get("commodity")
    variety = record.get("variety")
    grade = record.get("grade")

    arrival_date = parse_date(
        record.get("arrival_date")
    )

    min_price = record.get("min_price")
    max_price = record.get("max_price")
    modal_price = record.get("modal_price")

    # Get or create crop
    crop = get_or_create_crop(commodity)

    # Get or create market
    market = get_or_create_market(
        state,
        district,
        market_name
    )

    # Prevent duplicate records
    existing_price = MarketPrice.query.filter_by(
        market_id=market.id,
        crop_id=crop.id,
        variety=variety,
        grade=grade,
        arrival_date=arrival_date
    ).first()

    if existing_price:
        return False

    market_price = MarketPrice(
        market_id=market.id,
        crop_id=crop.id,
        variety=variety,
        grade=grade,
        arrival_date=arrival_date,
        min_price=min_price,
        max_price=max_price,
        modal_price=modal_price
    )

    db.session.add(market_price)

    return True


def ingest_data():
    print("Fetching government market data...")

    data = fetch_market_data()

    records = data.get("records", [])

    print(f"Records received: {len(records)}")

    inserted = 0
    skipped = 0

    for record in records:

        try:
            was_inserted = save_record(record)

            if was_inserted:
                inserted += 1
            else:
                skipped += 1

        except Exception as e:
            print("Error processing record:")
            print(record)
            print(e)

    db.session.commit()

    print("--------------------------------")
    print("Ingestion completed")
    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")
    print("--------------------------------")


if __name__ == "__main__":

    with app.app_context():
        ingest_data()