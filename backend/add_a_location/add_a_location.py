from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
from invokes import invoke_http  # Helper function to invoke HTTP services

app = Flask(__name__)
CORS(app)

# URLs for microservices
geocoding_URL = "http://localhost:5000/encode"
location_URL = "http://localhost:5002/locations"
userlocation_URL = "http://outsystems-server/userlocation/add_user_location"


@app.route("/add_location", methods=['POST'])
def add_location():
    """
    Composite microservice to add a location:
    1. Calls Geocoding microservice to get geocode (latitude, longitude).
    2. Calls Location microservice to save the location details.
    3. Calls UserLocation microservice to associate the location with a user.
    """
    if request.is_json:
        try:
            location_request = request.get_json()
            print("\nReceived a location request in JSON:", location_request)

            # Process the request
            result = process_add_location(location_request)
            return jsonify(result), result["code"]

        except Exception as e:
            # Handle unexpected errors
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "add_location.py internal error: " + ex_str
            }), 500

    # If input is not JSON
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def process_add_location(location_request):
    """
    Process the add location request:
    - Call Geocoding microservice.
    - Call Location microservice.
    - Call UserLocation microservice.
    """
    address = location_request.get("address")
    user_id = location_request.get("user_id")
    label = location_request.get("label")

    if not address or not user_id or not label:
        return {
            "code": 400,
            "message": "Missing required fields: 'address', 'user_id', and 'label'."
        }

    # Step 1: Call Geocoding Microservice
    print("\n-----Invoking Geocoding microservice-----")
    geocode_result = invoke_http(geocoding_URL, method="POST", json={"location": address})
    print("Geocode result:", geocode_result)

    if geocode_result["code"] not in range(200, 300):
        return {
            "code": geocode_result["code"],
            "message": f"Failed to get geocode for address '{address}'.",
            "data": geocode_result
        }

    latitude = geocode_result["latitude"]
    longitude = geocode_result["longitude"]
    country = geocode_result.get("country", "")
    state = geocode_result.get("state", "")
    city = geocode_result.get("city", "")
    neighbourhood = geocode_result.get("neighbourhood", "")

    # Step 2: Call Location Microservice
    print("\n-----Invoking Location microservice-----")
    location_payload = {
        "country": country,
        "state": state,
        "city": city,
        "neighbourhood": neighbourhood,
        "latitude": latitude,
        "longitude": longitude
    }
    
    location_result = invoke_http(location_URL, method="POST", json=location_payload)
    print("Location result:", location_result)

    if location_result["code"] not in range(200, 300):
        return {
            "code": location_result["code"],
            "message": f"Failed to save location details.",
            "data": location_result
        }

    location_id = location_result["location_id"]

    # Step 3: Call UserLocation Microservice
    print("\n-----Invoking UserLocation microservice-----")
    userlocation_payload = {
        "user_id": user_id,
        "location_id": location_id,
        "label": label,
        "address": address
    }
    
    userlocation_result = invoke_http(userlocation_URL, method="POST", json=userlocation_payload)
    print("UserLocation result:", userlocation_result)

    if userlocation_result["code"] not in range(200, 300):
        return {
            "code": userlocation_result["code"],
            "message": f"Failed to associate location with user.",
            "data": userlocation_result
        }

    # Return success response
    return {
        "code": 201,
        "message": f"Location added successfully for user {user_id}.",
        "data": {
            "geocoding_data": geocode_result,
            "location_data": location_result,
            "user_location_status": userlocation_result
        }
    }

@app.route("/")
def home():
    return "Add Location Service is running!"

if __name__ == "__main__":
    print("This is flask for adding a location...")
    app.run(host="0.0.0.0", port=5010, debug=True)
