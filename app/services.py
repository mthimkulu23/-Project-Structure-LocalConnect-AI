import os
import requests
# Import the geocoding function from your utils.py
from app.utils import geocode_location # Assuming app.utils can be imported like this

class LocationManager:
    def __init__(self):
        # No need for GOOGLE_PLACES_API_KEY here if we're using OpenCage for geocoding
        # self.google_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        # if not self.google_api_key:
        #     print("WARNING: GOOGLE_PLACES_API_KEY not found... Google Geocoding will not work.")
        #     self.geocoder_initialized = False
        # else:
        #     print("Google Geocoding client initialized (API key found).")
        #     self.geocoder_initialized = True
        
        # We will rely on app.utils.geocode_location which uses OPENCAGE_API_KEY
        # You might still want a check for OPENCAGE_API_KEY here if you initialize LocationManager in a place where utils.load_env_variables() hasn't run yet.
        # For simplicity, we'll assume utils.load_env_variables() runs early in your FastAPI app.
        print("LocationManager will use OpenCage Geocoding via app.utils.geocode_location.")

    async def geocode_location(self, location_name: str) -> dict | None:
        """
        Geocodes a location name to latitude and longitude using OpenCage Geocoding API (via utils.py).
        Returns a dictionary with 'latitude', 'longitude', and 'address' or None if unsuccessful.
        """
        # Call the geocode_location from utils.py
        coords = geocode_location(location_name) # This is a blocking call if not awaited
        if coords:
            lat, lon = coords
            # OpenCage doesn't directly return a formatted address in the same way,
            # you might need to adjust or perform a reverse geocode if you absolutely need it here.
            # For simplicity, we'll just return lat/lon and a dummy address for now.
            return {
                "latitude": lat,
                "longitude": lon,
                "address": f"Geocoded for {location_name}" # Placeholder for formatted address
            }
        return None

# Keep _search_google_places as is, but understand it will only work with billing.
# It's okay to leave it because search_local_services has the fallback.
def _search_google_places(query: str, location_coords: tuple = None, radius: int = 5000) -> list:
    """
    Searches Google Places API for establishments.
    Requires GOOGLE_PLACES_API_KEY in your .env file and active billing.
    Will return empty list if API key is not valid or billing not enabled.
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        print("WARNING: GOOGLE_PLACES_API_KEY not found. Google Places search disabled. (Billing probably not enabled).")
        return []

    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": api_key
    }

    if location_coords and isinstance(location_coords, tuple) and len(location_coords) == 2:
        params["location"] = f"{location_coords[0]},{location_coords[1]}"
        params["radius"] = radius 

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        data = response.json()

        if data.get("status") == "OK":
            places = []
            for result in data.get("results", []):
                places.append({
                    "name": result.get("name"),
                    "address": result.get("formatted_address"),
                    "rating": result.get("rating"),
                    "latitude": result.get("geometry", {}).get("location", {}).get("lat"),
                    "longitude": result.get("geometry", {}).get("location", {}).get("lng"),
                })
            return places
        else:
            print(f"Google Places search failed for: {query}. Status: {data.get('status')}. Message: {data.get('error_message', 'No error message provided')}. (Billing likely not enabled).")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error calling Google Places API for '{query}': {e}. This often means API key issues or billing not enabled.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during Google Places API call for '{query}': {e}")
        return []


async def search_local_services(service_type: str, location_coords: tuple = None, location_name: str = "") -> list:
    """
    Searches for local services based on type, optionally using geocoded coordinates.
    Attempts Google Places API (requires GOOGLE_PLACES_API_KEY and active billing).
    Falls back to mock data if Google Places fails or isn't configured/billed.
    """
    # Keep the GOOGLE_PLACES_API_KEY check. If it exists AND is billed, it will try Google.
    # Otherwise, it will fall back to mock data as desired.
    google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if google_places_api_key:
        print(f"Attempting to search '{service_type}' via Google Places API (requires valid API key and active billing)...")
        results = _search_google_places(service_type, location_coords)
        if results:
            return results

    print(f"Falling back to mock services for '{service_type}' (Google Places API likely failed, not configured, or billing not enabled)...")
    mock_services = {
        "police station": [
            {"name": "Johannesburg Central Police Station", "address": "123 Main St, Johannesburg", "rating": 4.0},
            {"name": "Rosebank Police Station", "address": "45 Oxford Rd, Rosebank", "rating": 3.8},
        ],
        "dentist": [
            {"name": "Smile Dental Clinic", "address": "789 Oak Ave, Cape Town", "rating": 4.5},
            {"name": "City Centre Dental", "address": "101 Pine St, Cape Town", "rating": 4.2},
        ],
        "restaurant": [
            {"name": "The Gourmet Grill", "address": "1 Broadway, Johannesburg", "rating": 4.7},
            {"name": "Italian Trattoria", "address": "2 High St, Johannesburg", "rating": 4.1},
        ],
        "event": [
            {"name": "Jazz Festival", "address": "Park Square, Durban", "date": "2025-08-10"},
            {"name": "Tech Conference", "address": "Convention Centre, Durban", "date": "2025-09-20"},
        ]
    }

    results = []
    if service_type in mock_services:
        for service in mock_services[service_type]:
         
            if location_name and location_name.lower() in service['address'].lower():
                results.append(service)
            elif not location_name: 
                results.append(service)

    return results

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # Load env vars for local testing

    async def test_geocoding_and_search():
        # Ensure OPENCAGE_API_KEY is in your .env for this test
        location_manager = LocationManager() # This will now rely on utils.geocode_location

        johannesburg_geocode_data = await location_manager.geocode_location("Johannesburg")
        johannesburg_coords = None
        if johannesburg_geocode_data:
            johannesburg_coords = (johannesburg_geocode_data['latitude'], johannesburg_geocode_data['longitude'])
            print(f"Johannesburg geocoded (via OpenCage): {johannesburg_geocode_data}")
        else:
            print("Johannesburg geocoding failed (OpenCage issue or API key missing). Using dummy coords for testing search fallback.")
            johannesburg_coords = (-26.2041, 28.0473) 

        cape_town_geocode_data = await location_manager.geocode_location("Cape Town")
        cape_town_coords = None
        if cape_town_geocode_data:
            cape_town_coords = (cape_town_geocode_data['latitude'], cape_town_geocode_data['longitude'])
            print(f"Cape Town geocoded (via OpenCage): {cape_town_geocode_data}")
        else:
            print("Cape Town geocoding failed (OpenCage issue or API key missing). Using dummy coords for testing search fallback.")
            cape_town_coords = (-33.9249, 18.4241) 


        print("\n--- Testing search_local_services (will attempt Google Places, then fallback to mock) ---")
       
        # These will attempt Google Places but likely fall back to mock unless billing is enabled.
        police_stations_jhb = await search_local_services('police station', location_coords=johannesburg_coords, location_name="Johannesburg")
        print(f"Police Stations in Johannesburg: {police_stations_jhb}")

        dentists_cpt = await search_local_services('dentist', location_coords=cape_town_coords, location_name="Cape Town")
        print(f"Dentists in Cape Town: {dentists_cpt}")

        restaurants_general = await search_local_services('restaurant', location_name="Johannesburg")
        print(f"Restaurants in Johannesburg (mock fallback): {restaurants_general}")

        events_general = await search_local_services('event')
        print(f"Events (mock fallback, no location specified): {events_general}")


    import asyncio
    asyncio.run(test_geocoding_and_search())