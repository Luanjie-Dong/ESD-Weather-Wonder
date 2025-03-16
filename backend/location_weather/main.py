# Location Weather API 
# Location Weather API  
# Endpoints:  
# 1. GET /get_weather/<LocationId>  
#    - Returns the latest 24-hour weather forecast for the location.  
#    - Response: {"hourlyForecast": [{datetime: "YYYY-MM-DD HH:MM", temperature: X, condition: "Sunny"}]}  
#  
# 2. GET /get_weather/<LocationId>/<DateTime>  
#    - Returns the weather forecast for a specific hour.  
#    - DateTime format: "YYYY-MM-DD HH:MM:SS"  
#    - Response: {"weather": {datetime: "YYYY-MM-DD HH:MM:SS", temperature: X, condition: "Cloudy"}}  
#  
# 3. POST /update_forecast/<LocationId>  
#    - Inserts a new 24h forecast into the database.  
#    - Request body: ForecastDay object  
#    - Response: {"message": "Weather data updated successfully."}  
#  
# ForecastDay object structure:  
#   public ForecastDay(LocalDate date, int date_epoch, Day day, Astro astro, Hour[] hour)
#   Note: Even though the entire object is currently being passed through, we only keep Hour[]
#
# location_weather table structure:
#   (pk)location_id: int
#   (pk)poll_datetime: datetime (as items are inserted using now() in supabase)
#   hourly_forecast: json (24h forecast)
#   forecast_day: date (date where forecast is for locally)

from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import requires_auth, add_auth_headers
import requests

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
LOCATION_SERVICE_URL = os.environ.get("LOCATION_SERVICE_URL", "http://localhost:5002") #fallback

app = Flask(__name__)
CORS(app)

def check_location_exists(location_id):
    # todo: add jwt auth if planning to roll for all services
    try:
        # Connection to location microservice running on 5002
        response = requests.get(f"{LOCATION_SERVICE_URL}/locations") 
        if not response.ok:
            return False, (jsonify({"error": "Failed to connect to location service"}), 503)
        location_data = response.json()
        if not location_data:
            return False, (jsonify({"error": "No locations found"}), 404)
        # Check if location_id exists in location_data's json information
        if not any(str(loc.get('location_id')) == str(location_id) for loc in location_data):
            return False, (jsonify({"error": "Location not found"}), 404)
        return True, None
    except Exception as e:
        return False, (jsonify({"error": f"Error checking location: {str(e)}"}), 500)

@app.route('/')
def home():
    print("Location Weather API is running!")
    return "Location Weather API is running!"

@app.route('/update_forecast/<location_id>', methods=['POST'])
# @requires_auth # decorator to ensure that there is a valid auth header present
def update_forecast(location_id):
    try:
        location_exists, error_response = check_location_exists(location_id)
        if not location_exists:
            return error_response
        # location = supabase.table('location').select('*').eq('location_id', location_id).execute()
        # if not location.data:
        #     return jsonify({"error": "Location not found"}), 404

        data = request.get_json()
        if not data or 'hour' not in data:
            return jsonify({"error": "Missing hourly forecast data"}), 400

        if not 'date' in data:
            return jsonify({"error": "Missing date in forecast data"}), 400

        # Extract date and format it as YYYY-MM-DD
        forecast_date = data['date']
        
        record = {
            'location_id': location_id,
            'forecast_day': forecast_date,
            'hourly_forecast': data['hour']
        }
        
        result = supabase.table('location_weather').insert(record).execute()
        return jsonify({"message": "Weather forecast updated successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error updating forecast: {str(e)}"}), 500

@app.route('/get_weather/<location_id>', methods=['GET'])
# @requires_auth # decorator to ensure that there is a valid auth header present
def get_latest_forecast(location_id):
    try:
        location_exists, error_response = check_location_exists(location_id)
        if not location_exists:
            return error_response
        # location = supabase.table('location').select('*').eq('location_id', location_id).execute()
        # if not location.data:
        #     return jsonify({"error": "Location not found"}), 404

        result = supabase.table('location_weather')\
            .select('*')\
            .eq('location_id', location_id)\
            .order('poll_datetime', desc=True)\
            .limit(1)\
            .execute()

        if not result.data:
            return jsonify({"error": "No weather data available for this location"}), 404

        forecast = result.data[0]
        return jsonify({
            "location_id": location_id,
            "forecast_day": forecast['forecast_day'],
            "hourlyForecast": forecast['hourly_forecast']
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error retrieving forecast: {str(e)}"}), 500

@app.route('/get_weather/date/<location_id>/<date>', methods=['GET'])
# @requires_auth # decorator to ensure that there is a valid auth header present
def get_forecast_by_date(location_id, date):
    try:
        location_exists, error_response = check_location_exists(location_id)
        if not location_exists:
            return error_response
        # location = supabase.table('location').select('*').eq('location_id', location_id).execute()
        # if not location.data:
        #     return jsonify({"error": "Location not found"}), 404

        # Parse and validate date format (YYYY-MM-DD)
        target_date = datetime.strptime(date, '%Y-%m-%d').date().isoformat()

        result = supabase.table('location_weather')\
            .select('*')\
            .eq('location_id', location_id)\
            .eq('forecast_day', target_date)\
            .order('poll_datetime', desc=True)\
            .limit(1)\
            .execute()

        if not result.data:
            return jsonify({"error": "No weather data found for the specified date"}), 404

        forecast = result.data[0]
        return jsonify({
            "location_id": location_id,
            "forecast_day": forecast['forecast_day'],
            "hourlyForecast": forecast['hourly_forecast']
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid date format. Expected: YYYY-MM-DD"}), 400
    except Exception as e:
        return jsonify({"error": f"Error retrieving forecast: {str(e)}"}), 500

@app.route('/get_weather/datetime/<location_id>/<dt_input>', methods=['GET'])
# @requires_auth # decorator to ensure that there is a valid auth header present
def get_forecast_by_datetime(location_id, dt_input):
    try:
        # Location check remains the same
        
        try:
            target_datetime = datetime.strptime(dt_input, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Expected: YYYY-MM-DD HH:MM:SS"}), 400
            
        target_date = target_datetime.date().isoformat()

        result = supabase.table('location_weather')\
            .select('*')\
            .eq('location_id', location_id)\
            .eq('forecast_day', target_date)\
            .order('poll_datetime', desc=True)\
            .limit(1)\
            .execute()

        if not result.data:
            return jsonify({"error": "No weather data found for the specified date"}), 404

        forecast = result.data[0]
        target_time = target_datetime.strftime('%Y-%m-%d %H:%M')
        
        hour_data = next(
            (hour for hour in forecast['hourly_forecast'] 
             if hour['time'] == target_time),
            None
        )

        if not hour_data:
            return jsonify({"error": "No weather data for specified datetime"}), 404

        return jsonify({
            "location_id": location_id,
            "forecast_day": forecast['forecast_day'],
            "weather": hour_data
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid datetime format. Expected: YYYY-MM-DD HH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": f"Error retrieving forecast: {str(e)}"}), 500

## Todo: Setup publishing to pika from here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)