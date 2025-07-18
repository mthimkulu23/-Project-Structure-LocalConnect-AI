import os
import requests

class LocationManager:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_PLACES_API_KEY") # We still try to get it
        if not self.google_api_key:
            print("WARNING: GOOGLE_PLACES_API_KEY not found in environment variables. Google Geocoding will not work.")
            self.geocoder_initialized = False
        else:
    
            print("Google Geocoding client initialized (API key found).")
            self.geocoder_initialized = True

    async def geocode_location(self, location_name: str) -> dict | None:
        """
        Geocodes a location name to latitude and longitude using Google Geocoding API.
        Returns a dictionary with 'latitude', 'longitude', and 'address' or None if unsuccessful.
        Will return None if API key is not valid or billing not enabled.
        """
        if not self.geocoder_initialized:
            print("Google Geocoding service not initialized or API key missing. Cannot geocode.")
            return None

        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": location_name,
            "key": self.google_api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status() 
            data = response.json()

            if data.get("status") == "OK" and data.get("results"):
                first_result = data["results"][0]
                latitude = first_result['geometry']['location']['lat']
                longitude = first_result['geometry']['location']['lng']
                formatted_address = first_result['formatted_address']
                return {
                    "latitude": latitude,
                    "longitude": longitude,
                    "address": formatted_address
                }
            else:
                print(f"Google Geocoding failed for: {location_name}. Status: {data.get('status')}. Message: {data.get('error_message', 'No error message provided')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling Google Geocoding API for '{location_name}': {e}. This often means API key issues or billing not enabled.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during Google Geocoding API call: {e}")
            return None

def _search_google_places(query: str, location_coords: tuple = None, radius: int = 5000) -> list:
    """
    Searches Google Places API for establishments.
    Requires GOOGLE_PLACES_API_KEY in your .env file and active billing.
    Will return empty list if API key is not valid or billing not enabled.
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        print("WARNING: GOOGLE_PLACES_API_KEY not found. Google Places search disabled.")
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
            print(f"Google Places search failed for: '{query}'. Status: {data.get('status')}. Message: {data.get('error_message', 'No error message provided')}")
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
    Prioritizes Google Places API if GOOGLE_PLACES_API_KEY is available and valid.
    Falls back to mock data if not.
    """
    google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if google_places_api_key:
        print(f"Attempting to search '{service_type}' via Google Places API (will only work if API key is valid and billed)...")
        results = _search_google_places(service_type, location_coords)
        if results:
            return results

    print(f"Falling back to mock services for '{service_type}' (Google API likely failed or not configured)...")
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


    async def test_geocoding_and_search():
        location_manager = LocationManager()
        johannesburg_coords = None
        johannesburg_geocode_data = await location_manager.geocode_location("Johannesburg")
        if johannesburg_geocode_data:
            johannesburg_coords = (johannesburg_geocode_data['latitude'], johannesburg_geocode_data['longitude'])
            print(f"Johannesburg geocoded: {johannesburg_geocode_data}")
        else:
            print("Johannesburg geocoding failed, using dummy coords for testing search fallback.")
            johannesburg_coords = (-26.2041, 28.0473) 


        cape_town_coords = None
        cape_town_geocode_data = await location_manager.geocode_location("Cape Town")
        if cape_town_geocode_data:
            cape_town_coords = (cape_town_geocode_data['latitude'], cape_town_geocode_data['longitude'])
            print(f"Cape Town geocoded: {cape_town_geocode_data}")
        else:
            print("Cape Town geocoding failed, using dummy coords for testing search fallback.")
            cape_town_coords = (-33.9249, 18.4241) 


        print("\n--- Testing search_local_services (will use Google Places/mock) ---")
       
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