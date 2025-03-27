#!/usr/bin/env python3

from flask import Flask, jsonify
import os
import json
import requests
import schedule
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ENV Configs
LOCATION_URL = os.getenv("LOCATION_URL", "http://location:5002")
WEATHER_URL = os.getenv("WEATHER_URL", "http://weather:8081")
LOCATION_WEATHER_URL = os.getenv("LOCATION_WEATHER_URL", "http://location_weather:5003")

@app.route('/')
def home():
    return "Poll Weather Forecast service is running!"

@app.route('/trigger-poll', methods=['POST'])
def trigger_poll():
    """Manually trigger the polling process"""
    try:
        result = poll_weather_forecasts()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error triggering poll: {str(e)}")
        return jsonify({"error": str(e)}), 500

def poll_weather_forecasts():
    """Poll weather forecasts for all registered locations"""
    logger.info("Starting weather forecast polling process")
    
    try:
        locations = get_all_locations()
        if not locations:
            logger.warning("No locations found to poll")
            return {"message": "No locations found to poll"}
        
        logger.info(f"Found {len(locations)} locations to poll")
        
        results = []
        for location in locations:
            try:
                location_id = location.get('location_id')
                country = location.get('country', '').strip()
                state = location.get('state', '').strip()
                city = location.get('city', '').strip()
                neighbourhood = location.get('neighbourhood', '').strip()
                
                # Debug location data
                logger.info(f"""
Location details for ID {location_id}:
- Country: '{country}'
- State: '{state}'
- City: '{city}'
- Neighbourhood: '{neighbourhood}'
                """)
                
                # Validate required fields
                if not (country and city):
                    logger.warning(f"Location ID {location_id}: Missing required fields - Country: '{country}', City: '{city}'")
                    continue
                
                forecast = get_forecast(country, state, city, neighbourhood)
                if not forecast:
                    logger.warning(f"No forecast data available for location ID: {location_id}")
                    continue
                
                # Log successful forecast retrieval
                logger.info(f"Successfully retrieved forecast for {city}, {state}, {country} (ID: {location_id})")
                
                update_result = update_location_weather(location_id, forecast)
                
                results.append({
                    "location_id": location_id,
                    "status": "success" if update_result else "failed",
                    "location": f"{city}, {state}, {country}"
                })
                
            except Exception as e:
                logger.error(f"""
Error processing location {location_id}:
- Error: {str(e)}
- Location data: {json.dumps(location, indent=2)}
                """)
                results.append({
                    "location_id": location.get('location_id'),
                    "status": "failed",
                    "error": str(e),
                    "location": f"{city}, {state}, {country}"
                })
        
        logger.info(f"Completed polling process. Processed {len(results)} locations.")
        return {
            "timestamp": datetime.now().isoformat(),
            "locations_processed": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in polling process: {str(e)}")
        raise

def get_all_locations():
    """Get all registered locations from the location service"""
    try:
        response = requests.get(f"{LOCATION_URL}/locations", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching locations: {str(e)}")
        return None

# Add a health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "services": {
            "location": check_service_health(LOCATION_URL),
            "weather": check_service_health(WEATHER_URL),
            "location_weather": check_service_health(LOCATION_WEATHER_URL)
        }
    }), 200

def check_service_health(service_url):
    """Check if a service is healthy"""
    try:
        response = requests.get(f"{service_url}/", timeout=5)
        return response.ok
    except:
        return False

# In the get_forecast function, add a retry mechanism
def get_forecast(country, state, city, neighbourhood, max_retries=3):
    """Get forecast from the weather service using GraphQL with retries"""
    retries = 0
    while retries < max_retries:
        try:
            # GraphQL query for forecast
            query = """
            query GetForecast($country: String!, $state: String!, $city: String!, $neighbourhood: String!) {
                getForecast(country: $country, state: $state, city: $city, neighbourhood: $neighbourhood) {
                    location {
                        name
                        region
                        country
                        localtime
                    }
                    forecast {
                        forecastDay {
                            date
                            date_epoch
                            day {
                                maxtemp_c
                                mintemp_c
                                avgtemp_c
                                maxwind_kph
                                totalprecip_mm
                                avghumidity
                                condition_text
                                condition_icon
                                condition_code
                            }
                            astro {
                                sunrise
                                sunset
                                moonrise
                                moonset
                                moon_phase
                            }
                            hour {
                                time
                                time_epoch
                                temp_c
                                condition_text
                                condition_icon
                                condition_code
                                wind_kph
                                wind_degree
                                wind_dir
                                pressure_mb
                                precip_mm
                                humidity
                                cloud
                                feelslike_c
                                windchill_c
                                heatindex_c
                                dewpoint_c
                                will_it_rain
                                chance_of_rain
                                will_it_snow
                                chance_of_snow
                                vis_km
                                gust_kph
                                uv
                            }
                        }
                    }
                }
            }
            """
            
            variables = {
                "country": country,
                "state": state,
                "city": city,
                "neighbourhood": neighbourhood
            }
            
            response = requests.post(
                f"{WEATHER_URL}/graphql",
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return None
                
            # Log successful forecast data
            forecast_data = data.get("data", {}).get("getForecast", {})
            if forecast_data:
                # logger.info(f"Received forecast data: {json.dumps(forecast_data, indent=2)}")
                logger.info("Sucessfully received forecast data")
            return forecast_data
        except requests.RequestException as e:
            retries += 1
            if retries >= max_retries:
                logger.error(f"Error fetching forecast after {max_retries} attempts: {str(e)}")
                return None
            logger.warning(f"Retry {retries}/{max_retries} after error: {str(e)}")
            time.sleep(2)  # Wait before retrying

def update_location_weather(location_id, forecast):
    """Update the location_weather service with the forecast data"""
    try:
        if not forecast or "forecast" not in forecast or "forecastDay" not in forecast["forecast"]:
            logger.warning(f"Invalid forecast data for location ID: {location_id}: {json.dumps(forecast, indent=2)}")
            return False
        
        forecastDay = forecast["forecast"]["forecastDay"][0]
        
        # Match location_weather's schema naming
        payload = {
            "forecast_day": forecastDay["date"],
            "hourly_forecast": forecastDay["hour"],
            "daily_forecast": forecastDay["day"],
            "astro_forecast": forecastDay["astro"]
        }
        # logger.info(f"Sending payload to location_weather service: {json.dumps(payload, indent=2)}")
        logger.info("Sending payload to location_weather service")
        
        try:
            # Send the update request
            response = requests.post(
                f"{LOCATION_WEATHER_URL}/update_forecast/{location_id}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Log the response details
            logger.info(f"Location weather update response: Status={response.status_code}, Content={response.text}")
            
            response.raise_for_status()
            logger.info(f"Successfully updated forecast for location ID: {location_id}")
            return True
            
        except requests.RequestException as e:
            logger.error(f"""
Error updating location_weather for ID {location_id}:
- Status Code: {getattr(e.response, 'status_code', 'N/A')}
- Error Message: {str(e)}
- Response Content: {getattr(e.response, 'text', 'N/A')}
- Request URL: {e.request.url}
- Request Body: {getattr(e.request, 'body', 'N/A')}
            """)
            return False
            
    except Exception as e:
        logger.error(f"Error preparing forecast data: {str(e)}")
        return False

def schedule_daily_poll():
    """Schedule the daily polling at midnight"""
    schedule.every().day.at("00:00").do(poll_weather_forecasts)
    logger.info("Scheduled daily polling at midnight (00:00)")

def run_scheduler():
    """Run the scheduler in a loop"""
    schedule_daily_poll()
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Start the scheduler in a separate thread
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5005, debug=True)