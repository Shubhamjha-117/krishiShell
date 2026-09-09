from app import app

from models.market import Market
from services.market_location_resolver import resolve_market


def main():

    with app.app_context():

        markets = Market.query.filter_by(
            state="Maharashtra"
        ).order_by(
            Market.district,
            Market.name
        ).all()

        print()
        print("========================================")
        print("KRISHISELL MARKET LOCATION RESOLVER")
        print("========================================")
        print(f"Markets: {len(markets)}")
        print()

        resolved = 0
        unresolved = 0

        for market in markets:

            print("----------------------------------------")

            print(
                f"Market   : {market.name}"
            )

            print(
                f"District : {market.district}"
            )

            result = resolve_market(market)

            print(
                f"Status   : {result['status']}"
            )

            print(
                f"Method   : {result['method']}"
            )

            print(
                f"Query    : {result['query']}"
            )

            if result["latitude"] is not None:

                print(
                    f"Candidate: "
                    f"{result['latitude']}, "
                    f"{result['longitude']}"
                )

                print(
                    f"Matched  : "
                    f"{result['display_name']}"
                )

                resolved += 1

            else:

                unresolved += 1

            print()

        print("========================================")
        print("SUMMARY")
        print("========================================")
        print(f"Candidates : {resolved}")
        print(f"Unresolved : {unresolved}")
        print("========================================")


if __name__ == "__main__":
    main()