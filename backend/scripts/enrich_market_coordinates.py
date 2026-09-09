import time
import requests

from app import app
from extentions import db
from models.market import Market


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "KrishiSell-Hackathon/1.0"
}


def geocode_market(market):
    query = f"{market.name}, {market.district}, Maharashtra, India"

    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        results = response.json()

        if not results:
            return None, None

        latitude = float(results[0]["lat"])
        longitude = float(results[0]["lon"])

        return latitude, longitude

    except Exception as e:
        print(f"Geocoding error for {market.name}: {e}")
        return None, None


def enrich_markets():

    markets = Market.query.filter_by(
        state="Maharashtra"
    ).order_by(
        Market.district,
        Market.name
    ).all()

    print(f"Markets found: {len(markets)}")
    print("--------------------------------")

    updated = 0
    failed = 0
    skipped = 0

    for market in markets:

        if market.latitude is not None and market.longitude is not None:
            print(
                f"SKIPPED | {market.name} | "
                f"{market.latitude}, {market.longitude}"
            )
            skipped += 1
            continue

        print(
            f"Searching | {market.name} | "
            f"{market.district}"
        )

        latitude, longitude = geocode_market(market)

        if latitude is not None and longitude is not None:

            market.latitude = latitude
            market.longitude = longitude

            updated += 1

            print(
                f"FOUND   | {latitude}, {longitude}"
            )

        else:
            failed += 1

            print("FAILED  | Coordinates not found")

        print("--------------------------------")

        # Respect geocoding service rate limits
        time.sleep(1)

    db.session.commit()

    print()
    print("================================")
    print("COORDINATE ENRICHMENT COMPLETE")
    print("================================")
    print(f"Updated : {updated}")
    print(f"Skipped : {skipped}")
    print(f"Failed  : {failed}")
    print("================================")


if __name__ == "__main__":

    with app.app_context():
        enrich_markets()