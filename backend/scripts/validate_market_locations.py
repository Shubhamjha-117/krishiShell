from app import app

from models.market import Market

from services.market_location_validator import (
    validate_result
)

from services.market_location_resolver import (
    resolve_market
)


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
        print("KRISHISELL MARKET CANDIDATE VALIDATION")
        print("========================================")
        print(f"Markets: {len(markets)}")
        print()

        total_candidates = 0
        high = 0
        medium = 0
        rejected = 0
        unresolved = 0

        for market in markets:

            print()
            print("========================================")
            print(
                f"MARKET: {market.name}"
            )
            print(
                f"DISTRICT: {market.district}"
            )
            print("========================================")

            candidates = list(
                resolve_market(market)
            )

            # Remove the final UNRESOLVED marker
            candidates = [
                candidate
                for candidate in candidates
                if candidate["status"] == "CANDIDATE"
            ]

            if not candidates:

                unresolved += 1

                print("❌ UNRESOLVED")

                continue

            for index, candidate in enumerate(
                candidates,
                start=1
            ):

                total_candidates += 1

                validation = validate_result(
                    market,
                    candidate
                )

                print()
                print(
                    f"Candidate #{index}"
                )

                print(
                    f"Query     : "
                    f"{candidate['query']}"
                )

                print(
                    f"Location  : "
                    f"{candidate['latitude']}, "
                    f"{candidate['longitude']}"
                )

                print(
                    f"Matched   : "
                    f"{candidate['display_name']}"
                )

                print(
                    f"Status    : "
                    f"{validation['status']}"
                )

                print(
                    f"Confidence: "
                    f"{validation['confidence']}"
                )

                print(
                    f"Reason    : "
                    f"{validation['reason']}"
                )

                if validation["status"] == "REJECTED":

                    rejected += 1

                elif validation["confidence"] == "HIGH":

                    high += 1

                elif validation["confidence"] == "MEDIUM":

                    medium += 1

        print()
        print()
        print("========================================")
        print("VALIDATION SUMMARY")
        print("========================================")
        print(
            f"Total candidates : {total_candidates}"
        )
        print(
            f"High confidence  : {high}"
        )
        print(
            f"Medium confidence: {medium}"
        )
        print(
            f"Rejected         : {rejected}"
        )
        print(
            f"Unresolved       : {unresolved}"
        )
        print("========================================")


if __name__ == "__main__":
    main()