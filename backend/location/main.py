from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)


# Supabase configuration (retrieved from environment variables)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "location"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route('/locations', methods=['POST'])
def add_location():
    data = request.get_json()

    # Validate input data
    required_fields = ['country', 'state', 'city', 'neighbourhood', 'latitude', 'longitude']
    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    # Check if location already exists in Supabase
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?country=eq.{data['country']}&state=eq.{data['state']}&city=eq.{data['city']}&neighbourhood=eq.{data['neighbourhood']}&latitude=eq.{data['latitude']}&longitude=eq.{data['longitude']}",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        existing_locations = response.json()
        if existing_locations:
            return jsonify({
                "message": "Location already exists", 
                "location": existing_locations[0],
                "location_id": existing_locations[0].get('location_id')
            }), 500

    # Generate unique location_id and insert new location into Supabase
    created_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # UTC timestamp
    payload = {
        "country": data['country'],
        "state": data['state'],
        "city": data['city'],
        "neighbourhood": data['neighbourhood'],
        "latitude": float(data['latitude']),
        "longitude": float(data['longitude']),
        "created_at": created_at
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=HEADERS,
        json=payload
    )

    if response.status_code == 201:
        # Retrieve the newly created location to get its ID
        new_location_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?created_at=eq.{created_at}",
            headers=HEADERS
        )
        if new_location_response.status_code == 200:
            new_location = new_location_response.json()[0]
            return jsonify({
                "message": "Location added successfully", 
                "location": new_location,
                "location_id": new_location.get('location_id')
            }), 201
        else:
            return jsonify({"error": "Location created but unable to retrieve ID"}), 500
    else:
        return jsonify({"error": response.json()}), response.status_code , 500


@app.route('/locations', methods=['GET'])
def get_locations():
    """
    Endpoint to retrieve all locations from Supabase.
    """
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
        headers=HEADERS
    )

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": response.json()}), response.status_code




@app.route('/')
def home():
    """
    Health check endpoint.
    """
    return "Microservice is running!", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
