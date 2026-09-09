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

    return {
        "market_id": market.id,
        "market_name": market.name,
        "distance_km": distance,
        "modal_price_per_quintal": price_record.modal_price,
        "price_per_kg": price_per_kg,
        "transport_cost_per_kg": transport_per_kg,
        "net_price_per_kg": net_price,
        "estimated_revenue": revenue,
        "arrival_date": price_record.arrival_date.isoformat()
    }
    