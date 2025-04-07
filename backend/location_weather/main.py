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
#    - Needs to also check for actual update to the forecast and then push notifications to users
#      publish to rabbitmq if there is a diff in the forecast

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
LOCATION_SERVICE_URL = os.environ.get("LOCATION_SERVICE_URL", "http://location:5002") #fallback

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

        data = request.get_json()
        if not data or 'hourly_forecast' not in data:
            return jsonify({"error": "Missing hourly forecast data"}), 400

        if not 'forecast_day' in data:
            return jsonify({"error": "Missing forecast_day in forecast data"}), 400

        if not 'daily_forecast' in data:
            return jsonify({"error": "Missing daily forecast data"}), 400

        if not 'astro_forecast' in data:
            return jsonify({"error": "Missing astro forecast data"}), 400

        record = {
            'location_id': location_id,
            'forecast_day': data['forecast_day'],
            'hourly_forecast': data['hourly_forecast'],
            'daily_forecast': data['daily_forecast'],
            'astro_forecast': data['astro_forecast']
        }
        
        result = supabase.table('location_weather').insert(record).execute()
        return jsonify({"message": "Weather forecast updated successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error updating forecast: {str(e)}"}), 500

@app.route('/publish_forecast/<location_id>', methods=['POST']) #publish endpoint to test 
# @requires_auth
def publish_forecast(location_id):
    try:
        location_exists, error_response = check_location_exists(location_id)
        if not location_exists:
            return error_response

        # Get the latest forecast for the location
        result = supabase.table('location_weather')\
            .select('*')\
            .eq('location_id', location_id)\
            .order('poll_datetime', desc=True)\
            .limit(1)\
            .execute()

        if not result.data:
            return jsonify({"error": "No forecast data available for this location"}), 404

        record = result.data[0]
        
        # Publish forecast update to RabbitMQ
        publish_success = publish_forecast_update(location_id, record)
        if not publish_success:
            return jsonify({"error": "Failed to publish forecast update to message queue"}), 500
            
        return jsonify({"message": "Forecast published successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error publishing forecast: {str(e)}"}), 500

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

        if not result.data:
            return jsonify({"error": "No weather data found for the specified date"}), 404

        forecast = result.data[0]
        return jsonify({
            "location_id": location_id,
            "forecast_day": forecast['forecast_day'],
            "poll_datetime": forecast['poll_datetime'],
            "hourlyForecast": forecast['hourly_forecast'],
            "dailyForecast": forecast['daily_forecast'],
            "astroForecast": forecast['astro_forecast']
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error retrieving forecast: {str(e)}"}), 500
    
@app.route('/get_user_weather/<location_ids>', methods=['GET'])
def get_user_forecast(location_ids):
    try:
        location_id_list = location_ids.split(',')
        for location_id in location_id_list:
            location_exists, error_response = check_location_exists(location_id)
            if not location_exists:
                return error_response

        result = supabase.table('location_weather')\
            .select('*')\
            .in_('location_id', location_id_list)\
            .order('poll_datetime', desc=True)\
            .execute()

        if not result.data:
            return jsonify({"error": "No weather data available for the specified locations"}), 404

        forecasts = []
        for forecast in result.data:
            forecasts.append({
                "location_id": forecast['location_id'],
                "forecast_day": forecast['forecast_day'],
                "poll_datetime": forecast['poll_datetime'],
                "hourlyForecast": forecast['hourly_forecast'],
                "dailyForecast": forecast['daily_forecast'],
                "astroForecast": forecast['astro_forecast']
            })

        return jsonify(forecasts), 200

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
            "forecast_day": target_date,
            "poll_datetime": forecast['poll_datetime'],
            "hourlyForecast": forecast['hourly_forecast'],
            "dailyForecast": forecast['daily_forecast'],
            "astroForecast": forecast['astro_forecast']
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
            "weather": hour_data,
            "dailyForecast": forecast['daily_forecast'],
            "astroForecast": forecast['astro_forecast']
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid datetime format. Expected: YYYY-MM-DD HH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": f"Error retrieving forecast: {str(e)}"}), 500

@app.route('/get_all_weather', methods=['GET'])
# @requires_auth
def get_all_latest_forecasts():
    try:
        # Get all locations first
        response = requests.get(f"{LOCATION_SERVICE_URL}/locations")
        if not response.ok:
            return jsonify({"error": "Failed to connect to location service"}), 503
        
        locations = response.json()
        if not locations:
            return jsonify({"error": "No locations found"}), 404

        all_forecasts = []
        for location in locations:
            location_id = location['location_id']
            result = supabase.table('location_weather')\
                .select('*')\
                .eq('location_id', location_id)\
                .order('poll_datetime', desc=True)\
                .limit(1)\
                .execute()

            if result.data:
                forecast = result.data[0]
                all_forecasts.append({
                    "location_id": location_id,
                    "forecast_day": forecast['forecast_day'],
                    "poll_datetime": forecast['poll_datetime'],
                    "hourlyForecast": forecast['hourly_forecast'],
                    "dailyForecast": forecast['daily_forecast'],
                    "astroForecast": forecast['astro_forecast']
                })

        return jsonify({"forecasts": all_forecasts}), 200

    except Exception as e:
        return jsonify({"error": f"Error retrieving forecasts: {str(e)}"}), 500

# RabbitMQ Configuration
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "myuser")
RABBITMQ_PASS = os.environ.get("RABBITMQ_PASS", "secret")

def publish_forecast_update(location_id, forecast_data):
    import pika
    import json
    connection = None
    try:
        print(f"Attempting to connect to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials,
            heartbeat=600,
            connection_attempts=5,  # Increased retries
            retry_delay=2  # Decreased delay between retries
        )
        
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        print("Successfully connected to RabbitMQ")

        EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME", "esd-weatherwonder")
        print(f"Using exchange: {EXCHANGE_NAME}")
        
        # Declare exchange
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type='topic',
            durable=True
        )

        # Ensure queue exists
        queue_name = "Trigger_Forecast_Process"
        print(f"Declaring queue: {queue_name}")
        channel.queue_declare(
            queue=queue_name,
            durable=True,
            arguments={"x-max-priority": 10}
        )
        
        routing_key = 'location.weather.update'
        print(f"Binding queue with routing key: {routing_key}")
        channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=queue_name,
            routing_key="#.update"  # Binding pattern
        )

        message = {
            "location_id": location_id,
            "forecast_day": forecast_data['forecast_day'],
            "poll_datetime": forecast_data['poll_datetime'],
            "daily_forecast": forecast_data['daily_forecast']
        }
        
        print(f"Publishing message for location_id: {location_id}")
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        print("Message published successfully")
        return True

    except pika.exceptions.AMQPConnectionError as e:
        print(f"AMQP Connection Error: {str(e)}")
        print(f"Failed to connect to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        return False
    except pika.exceptions.AMQPChannelError as e:
        print(f"AMQP Channel Error: {str(e)}")
        print("Failed to create/bind channel")
        return False
    except Exception as e:
        print(f"Unexpected error in publish_forecast_update: {str(e)}")
        return False
    finally:
        if connection and not connection.is_closed:
            try:
                connection.close()
                print("RabbitMQ connection closed")
            except Exception as e:
                print(f"Error closing connection: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)