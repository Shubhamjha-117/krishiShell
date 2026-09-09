from services.logistics_services import calculate_distance, calculate_transport_cost_per_kg

def calculate_price_per_kg(modal_price):
    if modal_price is None:
        return None

    return modal_price / 100


def calculate_net_price(
    modal_price,
    transport_cost_per_kg
):
    price_per_kg = calculate_price_per_kg(modal_price)

    if price_per_kg is None:
        return None
    
    if transport_cost_per_kg is None:
        return price_per_kg

    return price_per_kg - transport_cost_per_kg


def calculate_revenue(
    quantity_kg,
    net_price_per_kg
):
    if net_price_per_kg is None:
        return None

    return quantity_kg * net_price_per_kg



def evaluate_market(
    price_record,
    farmer_lat,
    farmer_lon,
    quantity_kg
):

    market = price_record.market

    if (
        market is None
        or price_record.modal_price is None
        or price_record.arrival_date is None
    ):
        return None
    if market.latitude is None or market.longitude is None:
        return None

    distance = calculate_distance(
        farmer_lat,
        farmer_lon,
        market.latitude,
        market.longitude
    )

    transport_per_kg = calculate_transport_cost_per_kg(
        distance,
        quantity_kg
    )

    price_per_kg = calculate_price_per_kg(
        price_record.modal_price
    )

    net_price = calculate_net_price(
        price_record.modal_price,
        transport_per_kg
    )

    revenue = calculate_revenue(
        quantity_kg,
        net_price
    )

    if distance is None or net_price is None or revenue is None:
        return None

    return {
        "market_id": market.id,
        "market_name": market.name,
        "distance_km": distance,
        "modal_price_per_quintal": price_record.modal_price,
        "price_per_kg": price_per_kg,
        "transport_cost_per_kg": transport_per_kg,
        "net_price_per_kg": net_price,
        "estimated_net_realisation": revenue,
        "estimated_revenue": revenue,
        "arrival_date": price_record.arrival_date.isoformat()
    }


def rank_markets(price_records, farmer_lat, farmer_lon, quantity_kg):
    """Evaluate usable records and rank by net realisation."""
    evaluations_by_market = {}
    for price_record in price_records:
        try:
            evaluation = evaluate_market(
                price_record,
                farmer_lat,
                farmer_lon,
                quantity_kg
            )
        except (TypeError, ValueError, AttributeError):
            evaluation = None
        if evaluation is not None:
            current = evaluations_by_market.get(evaluation["market_id"])
            if (
                current is None
                or evaluation["estimated_net_realisation"]
                > current["estimated_net_realisation"]
            ):
                evaluations_by_market[evaluation["market_id"]] = evaluation

    return sorted(
        evaluations_by_market.values(),
        key=lambda result: (
            result["estimated_net_realisation"],
            result["net_price_per_kg"],
            -result["distance_km"]
        ),
        reverse=True
    )
    