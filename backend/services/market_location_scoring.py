from services.market_aliases import MARKET_LOCALITY_ALIASES


STRONG_MARKET_TERMS = [
    "market yard",
    "agricultural produce market",
    "krushi utpanna",
    "krushi utpanna bajar",
    "apmc market",
]


BAD_TERMS = [
    "school",
    "hospital",
    "bank",
    "petrol pump",
    "restaurant",
    "hotel",
    "college",
    "temple",
    "church",
    "mosque",
]


def score_candidate(market, candidate):

    display_name = (
        candidate.get("display_name") or ""
    ).lower()

    score = 0
    reasons = []

    # --------------------------------
    # 1. Reject obvious non-market objects
    # --------------------------------

    for term in BAD_TERMS:
        if term in display_name:
            return {
                "score": -100,
                "status": "REJECTED",
                "reasons": [f"non_market:{term}"]
            }

    # --------------------------------
    # 2. Market-yard evidence
    # --------------------------------

    strong_market_term = None

    for term in STRONG_MARKET_TERMS:
        if term in display_name:
            strong_market_term = term
            break

    if strong_market_term:
        score += 50
        reasons.append(
            f"strong_market_term:{strong_market_term}"
        )
    else:
        # "APMC Park" should NOT count as a market yard.
        if "apmc" in display_name:
            score += 15
            reasons.append("apmc_only")

    # --------------------------------
    # 3. Expected locality
    # --------------------------------

    expected_localities = MARKET_LOCALITY_ALIASES.get(
        market.name,
        []
    )

    locality_match = False

    for locality in expected_localities:
        if locality.lower() in display_name:
            locality_match = True
            score += 40
            reasons.append(
                f"locality_match:{locality}"
            )
            break

    if not locality_match:
        score -= 40
        reasons.append("expected_locality_not_found")

    # --------------------------------
    # 4. Market name match
    # --------------------------------

    market_name = (
        market.name
        .lower()
        .replace("apmc", "")
        .strip()
    )

    if market_name and market_name in display_name:
        score += 10
        reasons.append("market_name_match")

    # --------------------------------
    # Final classification
    # --------------------------------

    if (
        strong_market_term
        and locality_match
        and score >= 80
    ):
        status = "VERIFIED"

    elif locality_match and score >= 40:
        status = "REVIEW"

    else:
        status = "REJECTED"

    return {
        "score": score,
        "status": status,
        "reasons": reasons,
    }