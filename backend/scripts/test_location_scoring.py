from app import app

from models.market import Market

from services.market_location_resolver import (
    resolve_market
)

from services.market_location_scoring import (
    score_candidate
)


def main():

    with app.app_context():

        markets = Market.query.filter_by(
            state="Maharashtra"
        ).order_by(
            Market.district,
            Market.name
        ).all()

        for market in markets:

            print()
            print("=" * 60)
            print(market.name)
            print("=" * 60)

            candidates = [
                candidate
                for candidate in resolve_market(market)
                if candidate["status"] == "CANDIDATE"
            ]

            if not candidates:

                print("UNRESOLVED")
                continue

            for candidate in candidates:

                result = score_candidate(
                    market,
                    candidate
                )

                print()
                print(
                    "Candidate:",
                    candidate["display_name"]
                )

                print(
                    "Coordinates:",
                    candidate["latitude"],
                    candidate["longitude"]
                )

                print(
                    "Score:",
                    result["score"]
                )

                print(
                    "Status:",
                    result["status"]
                )

                print(
                    "Reasons:",
                    ", ".join(
                        result["reasons"]
                    )
                )


if __name__ == "__main__":
    main()