import re
import time
import requests


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "KrishiSell-Hackathon/1.0"
}


# Known town/location corrections.
# These are LOCATION HINTS, not coordinates.
LOCATION_HINTS = {
    "APMC Kopargaon": "Kopargaon, Maharashtra, India",
    "APMC Rahata": "Rahata, Maharashtra, India",
    "APMC Sangamner": "Sangamner, Maharashtra, India",
    "APMC Akola": "Akola, Maharashtra, India",
    "APMC Malkapur": "Malkapur, Buldhana, Maharashtra, India",
    "APMC Jalgaon": "Jalgaon, Maharashtra, India",
    "APMC Kolhapur": "Kolhapur, Maharashtra, India",

    "APMC Chandwad": "Chandwad, Nashik, Maharashtra, India",
    "APMC Dindori": "Dindori, Nashik, Maharashtra, India",
    "APMC Kalvan": "Kalwan, Nashik, Maharashtra, India",
    "APMC Nampur": "Nampur, Nashik, Maharashtra, India",
    "APMC Nasik": "Nashik, Maharashtra, India",
    "APMC Pimpalgaon Baswant": "Pimpalgaon Baswant, Nashik, Maharashtra, India",
    "APMC Satana": "Satana, Nashik, Maharashtra, India",
    "APMC Sinner": "Sinnar, Nashik, Maharashtra, India",
    "APMC Umrane": "Umrane, Nashik, Maharashtra, India",

    "Lasalgaon(Niphad)": "Lasalgaon, Niphad, Nashik, Maharashtra, India",
    "Lasalgaon(Vinchur)": "Vinchur, Nashik, Maharashtra, India",

    "APMC Indapur": "Indapur, Pune, Maharashtra, India",
    "APMC Khed": "Khed, Pune, Maharashtra, India",

    "APMC Karad": "Karad, Satara, Maharashtra, India",
    "APMC Satara": "Satara, Maharashtra, India",
    "APMC Vaduj": "Vaduj, Satara, Maharashtra, India",
    "APMC Vai": "Wai, Satara, Maharashtra, India",

    "APMC Solapur": "Solapur, Maharashtra, India",
}


def normalize_name(name):
    """
    Normalize market names for matching.
    """

    name = name.strip()

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name


def geocode(query):

    params = {
        "q": query,
        "format": "json",
        "limit": 3,
        "countrycodes": "in"
    }

    try:

        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        print(f"Geocoding error: {e}")

        return []


def resolve_market(market):

    queries = build_queries(market)

    for query in queries:

        print(f"  Trying: {query}")

        results = geocode(query)

        time.sleep(1)

        for result in results:

            latitude = float(result["lat"])
            longitude = float(result["lon"])

            yield {
                "status": "CANDIDATE",
                "method": "market_query",
                "query": query,
                "latitude": latitude,
                "longitude": longitude,
                "display_name": result.get(
                    "display_name"
                )
            }

    yield {
        "status": "UNRESOLVED",
        "method": None,
        "query": None,
        "latitude": None,
        "longitude": None,
        "display_name": None
    }
    

    
def build_queries(market):

    name = market.name.strip()

    # Remove trailing/leading whitespace
    clean_name = name.strip()

    # Known aliases for difficult markets
    aliases = {
        "APMC Nagpur": [
            "Kalamna Market Yard Nagpur Maharashtra"
        ],

        "APMC Pune": [
            "Market Yard Gultekdi Pune Maharashtra"
        ],

        "Pune(Moshi)": [
            "APMC Moshi Market Yard Pune Maharashtra"
        ],

        "Pune(Pimpri)": [
            "APMC Pimpri Market Yard Pune Maharashtra"
        ],

        "Pune(Manjri)": [
            "APMC Manjri Market Yard Pune Maharashtra"
        ],

        "Pune(Khadiki)": [
            "APMC Khadki Market Yard Pune Maharashtra"
        ],

        "APMC Hingna": [
            "APMC Hingna Nagpur Maharashtra"
        ],

        "Mumbai-Onion & Potato Market": [
            "APMC Onion Potato Market Vashi Maharashtra"
        ],

        "Amrawati(Frui & Veg. Market)": [
            "APMC Fruit Vegetable Market Amravati Maharashtra"
        ],
    }

    if clean_name in aliases:
        return aliases[clean_name]

    queries = []

    # Original market name
    queries.append(
        f"{clean_name}, "
        f"{market.district}, "
        f"Maharashtra, India"
    )

    # Market yard wording
    queries.append(
        f"{clean_name} Market Yard, "
        f"{market.district}, "
        f"Maharashtra, India"
    )

    # Agricultural Produce Market
    queries.append(
        f"Agricultural Produce Market Committee "
        f"{clean_name}, "
        f"{market.district}, "
        f"Maharashtra, India"
    )

    return queries