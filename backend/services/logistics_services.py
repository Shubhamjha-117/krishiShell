DEFAULT_COST_PER_KM = 20

def calculate_distance(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2
    
    if None in (lat1, lon1, lat2, lon2):
        return None
    if not all(-90 <= value <= 90 for value in (lat1, lat2)):
        return None
    if not all(-180 <= value <= 180 for value in (lon1, lon2)):
        return None
    
    R = 6371.0
    
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = (
        sin(dlat / 2) ** 2 
        + cos(lat1) 
        * cos(lat2) 
        * sin(dlon / 2) ** 2
    )
    
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def calculate_transport_cost(
    distance_km,
    cost_per_km=DEFAULT_COST_PER_KM
):
    

    if distance_km is None:
        return None

    return distance_km * cost_per_km


def calculate_transport_cost_per_kg(
    distance_km,
    quantity_kg,
    cost_per_km=DEFAULT_COST_PER_KM
):
    if distance_km is None:
        return None

    if quantity_kg <= 0:
        return None

    total_cost = distance_km * cost_per_km

    return total_cost / quantity_kg