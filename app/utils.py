import os
from dotenv import load_dotenv
import re
import requests # For geocoding

def load_env_variables():
    """Loads environment variables from the .env file."""
    load_dotenv()

def parse_query_for_intent(query: str) -> tuple:
    """
    Parses the user query to extract intent (e.g., "search_service")
    and relevant entities (service type, location).
    This is a very basic rule-based parser. For production, consider using
    a more robust NLP library (e.g., spaCy, NLTK with trained models, or a simple NLU service).
    """
    query = query.lower()
    service_type = None
    location = None
    intent = "general_query"

    # Keywords for service search
    service_keywords = {
        "police station": ["police station", "cop shop", "saps"],
        "dentist": ["dentist", "dental clinic", "tooth doctor"],
        "restaurant": ["restaurant", "eatery", "cafe", "food"],
        "event": ["event", "show", "festival", "concert"],
        # Add more service types as needed
    }

    # Identify service type
    for svc_type, keywords in service_keywords.items():
        for keyword in keywords:
            if keyword in query:
                service_type = svc_type
                intent = "search_service"
                break
        if service_type:
            break

    # Extract location (very basic regex, needs improvement for real-world use)
    # Looks for "in [city]" or "near [city]"
    location_patterns = [
        r"in\s+([a-zA-Z\s]+)",
        r"near\s+([a-zA-Z\s]+)"
    ]
    for pattern in location_patterns:
        match = re.search(pattern, query)
        if match:
            location = match.group(1).strip()
            # Remove the found location part from the query for cleaner service_type extraction if needed
            query = query.replace(match.group(0), "").strip()
            break
    
    # If no specific location found, but "me" or "here" is used, suggest "current_location"
    if not location and ("near me" in query or "here" in query):
        location = "current_location"


    # If a service type was identified, try to refine the location further if not already found
    # This part can become complex with real NLP, for now, we rely on the above.

    return intent, service_type, location

def geocode_location(address: str) -> tuple | None:
    """
    Geocodes an address string to latitude and longitude coordinates
    using the OpenCage Geocoding API (or similar).
    Requires OPENCAGE_API_KEY in your .env file.
    """
    api_key = os.getenv("OPENCAGE_API_KEY")
    if not api_key:
        print("OPENCAGE_API_KEY not found. Geocoding disabled.")
        return None

    base_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": address,
        "key": api_key,
        "limit": 1 # We only need the top result
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data and data.get("results"):
            geometry = data["results"][0]["geometry"]
            return geometry["lat"], geometry["lon"]
        else:
            print(f"No geocoding results for: {address}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling geocoding API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during geocoding: {e}")
        return None

if __name__ == "__main__":
    load_env_variables() # Ensure .env is loaded for testing

    print("Testing parse_query_for_intent:")
    print(parse_query_for_intent("Police Station in Johannesburg"))
    print(parse_query_for_intent("Top-rated dentists near me"))
    print(parse_query_for_intent("Where can I find a good restaurant in Cape Town?"))
    print(parse_query_for_intent("Tell me about the weather"))
    print("-" * 30)

    print("Testing geocode_location (requires OPENCAGE_API_KEY in .env):")
    johannesburg_coords = geocode_location("Johannesburg")
    print(f"Johannesburg coords: {johannesburg_coords}")
    london_coords = geocode_location("London, UK")
    print(f"London coords: {london_coords}")
    invalid_location = geocode_location("asdfasdfasdf")
    print(f"Invalid location coords: {invalid_location}")