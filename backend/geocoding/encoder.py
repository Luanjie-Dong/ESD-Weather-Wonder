import requests
from dotenv import load_dotenv
import os
from urllib.parse import quote
load_dotenv()


def encode_location_by_name(location_name):

    url = "https://api.opencagedata.com/geocode/v1/json?"
    api_key = os.environ.get("GEOCODING_API_KEY")
    params = {
        "q": location_name,
        "key": api_key
    }
  
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  

        try:
            location_data = response.json()
        except ValueError:
            print(f"Invalid JSON response for {location_name}")
            return None
        

        if "results" in location_data and len(location_data["results"]) > 0:
            result = location_data["results"][0]
            return {
                "latitude": result["geometry"]["lat"],
                "longitude": result["geometry"]["lng"],
                "country": result.get("components", {}).get("country", "Unknown"),
                "county": result["components"].get("county", ""),
                "formatted_location": result['formatted']
            }
        else:
            print(f"No results found for {location_name}")
            return None
        

    except requests.exceptions.RequestException as e:
            print(f"Error encoding location data for {location_name}: {e}")

    

def decode_location(lat,lon):
    url = "https://api.opencagedata.com/geocode/v1/json?"
    api_key = os.environ.get("GEOCODING_API_KEY")

    lat_lon = f"{lat},{lon}"
    encoded_lat_lon = quote(lat_lon)

    params = {
        "q": encoded_lat_lon,
        "key": api_key
    }
  
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  

        try:
            location_data = response.json()
        except ValueError:
            print(f"Invalid JSON response for {lat} , {lon}")
            return None
        

        if "results" in location_data and len(location_data["results"]) > 0:
            result = location_data["results"][0]
            return {
                "location": result.get("formatted","")
            }
        else:
            print(f"No results found for {lat} , {lon}")
            return None
        

    except requests.exceptions.RequestException as e:
            print(f"Error encoding location data for {lat} , {lon}: {e}")


if __name__=="__main__":
    # lat = "-31.9842784"
    # lon = "115.7541052"
    # decoded = decode_location(lat,lon)
    # print(decoded)


    location = "57 Margaret St Cottesloe"
    encoded = encode_location_by_name(location)
    print(encoded)