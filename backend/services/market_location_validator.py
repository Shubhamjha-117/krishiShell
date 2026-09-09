from math import radians, sin, cos, sqrt, atan2


# Approximate Maharashtra bounding box.
# This is only the first sanity check.
MAHARASHTRA_BOUNDS = {
    "min_lat": 15.5,
    "max_lat": 22.1,
    "min_lon": 72.5,
    "max_lon": 80.9,
}


# District/town anchors.
# These are NOT market coordinates.
# They are only used to check whether a geocoder result
# is reasonably close to the expected district.
DISTRICT_ANCHORS = {
    "Ahilyanagar": (19.09, 74.74),
    "Akola": (20.70, 77.01),
    "Amarawati": (20.94, 77.76),
    "Buldhana": (20.53, 76.18),
    "Chandrapur": (19.96, 79.30),
    "Chattrapati Sambhajinagar": (19.88, 75.34),
    "Dhule": (20.90, 74.77),
    "Jalgaon": (21.01, 75.56),
    "Kolhapur": (16.70, 74.24),
    "Mumbai": (19.08, 72.88),
    "Nagpur": (21.15, 79.09),
    "Nashik": (20.01, 73.79),
    "Pune": (18.52, 73.86),
    "Satara": (17.68, 74.02),
    "Solapur": (17.66, 75.91),
}


def calculate_distance_km(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate straight-line distance between two coordinates.
    """

    earth_radius = 6371.0

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

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


def validate_bounds(latitude, longitude):

    if latitude is None or longitude is None:
        return False, "missing_coordinates"

    if not (
        MAHARASHTRA_BOUNDS["min_lat"]
        <= latitude
        <= MAHARASHTRA_BOUNDS["max_lat"]
    ):
        return False, "outside_maharashtra_latitude"

    if not (
        MAHARASHTRA_BOUNDS["min_lon"]
        <= longitude
        <= MAHARASHTRA_BOUNDS["max_lon"]
    ):
        return False, "outside_maharashtra_longitude"

    return True, None


def validate_district_proximity(
    market,
    latitude,
    longitude
):

    anchor = DISTRICT_ANCHORS.get(
        market.district
    )

    if anchor is None:
        return True, None, None

    anchor_lat, anchor_lon = anchor

    distance = calculate_distance_km(
        anchor_lat,
        anchor_lon,
        latitude,
        longitude
    )

    # Very large distance means the geocoder
    # probably returned the wrong place.
    if distance > 100:
        return False, "too_far_from_district", distance

    return True, None, distance


def validate_result(
    market,
    candidate
):

    latitude = candidate.get("latitude")
    longitude = candidate.get("longitude")

    # -----------------------------------------
    # Check 1: coordinates exist
    # -----------------------------------------

    if latitude is None or longitude is None:

        return {
            "status": "REJECTED",
            "confidence": "LOW",
            "reason": "missing_coordinates"
        }

    # -----------------------------------------
    # Check 2: Maharashtra bounds
    # -----------------------------------------

    valid, reason = validate_bounds(
        latitude,
        longitude
    )

    if not valid:

        return {
            "status": "REJECTED",
            "confidence": "LOW",
            "reason": reason
        }

    # -----------------------------------------
    # Check 3: expected district proximity
    # -----------------------------------------

    valid, reason, distance = (
        validate_district_proximity(
            market,
            latitude,
            longitude
        )
    )

    if not valid:

        return {
            "status": "REJECTED",
            "confidence": "LOW",
            "reason": reason,
            "district_distance_km": round(
                distance,
                2
            )
        }

    # -----------------------------------------
    # Check 4: inspect matched object
    # -----------------------------------------

    display_name = (
        candidate.get("display_name")
        or ""
    ).lower()

    suspicious_objects = [
        "school",
        "hospital",
        "bank",
        "petrol pump",
        "school",
        "college",
        "restaurant",
        "hotel",
    ]

    for object_name in suspicious_objects:

        if object_name in display_name:

            return {
                "status": "REJECTED",
                "confidence": "LOW",
                "reason": (
                    f"matched_non_market_object:"
                    f"{object_name}"
                ),
                "district_distance_km": (
                    round(distance, 2)
                    if distance is not None
                    else None
                )
            }

    # -----------------------------------------
    # Candidate passed basic checks
    # -----------------------------------------

    if distance is not None and distance <= 50:

        confidence = "HIGH"

    else:

        confidence = "MEDIUM"

    return {
        "status": "REVIEW",
        "confidence": confidence,
        "reason": "passed_basic_validation",
        "district_distance_km": (
            round(distance, 2)
            if distance is not None
            else None
        )
    }