# Location Weather API
# params
#     LocationId: string
#     DateTime(optional): datetime (optional)
# returns
#     Weather: json
# This service is intended to provide the following endpoints
# Updating weather forecast for a a given location and datetime (so that we can record them in a timeseries)
# Getting weather forecast for a given location and datetime (if no datetime is given, default to latest forecast)
# LocationId and DateTime is dependent on mh's implementation but i'll assume that the input will look like what openweather returns
# https://openweathermap.org/current#example_JSON

from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

weather_data = {
    "east-coast-road": {
        datetime.fromisoformat("2025-03-05T12:00:00"): {
            "temp": 28.5,
            "humidity": 85,
            "description": "partly cloudy",
            "wind_speed": 3.5,
            "feels_like": 32.1,
        },
        datetime.fromisoformat("2025-03-06T12:00:00"): {
            "temp": 30.2,
            "humidity": 82,
            "description": "scattered clouds",
            "wind_speed": 4.1,
            "feels_like": 33.8,
        },
    },
    "east-coast-park": {
        datetime.fromisoformat("2025-03-05T12:00:00"): {
            "temp": 27.8,
            "humidity": 88,
            "description": "light rain",
            "wind_speed": 5.2,
            "feels_like": 31.3,
        },
        datetime.fromisoformat("2025-03-06T12:00:00"): {
            "temp": 29.1,
            "humidity": 86,
            "description": "overcast clouds",
            "wind_speed": 5.8,
            "feels_like": 32.5,
        },
    },
}


@app.route("/update_weather/<location_id>", methods=["POST"])
def update_weather(location_id):
    data = request.get_json()
    if not data or "datetime" not in data or "weather" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    try:
        date_time = datetime.fromisoformat(data["datetime"])
        weather_info = data["weather"]

        if location_id not in weather_data:
            # this will force the weather update for a unsaved location as it is an internal API
            # should have no user impact if location_id is not found, missing etc
            weather_data[location_id] = {}  # todo: update this to db conn

        weather_data[location_id][date_time] = weather_info
        return jsonify({"message": "Weather forecast updated successfully"}), 200

    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400


# Two routes to allow for datetime to be a optional var
@app.route("/get_weather/<location_id>", methods=["GET"])
@app.route("/get_weather/<location_id>/<dt_input>", methods=["GET"])
def get_weather(location_id, dt_input=None):  # Changed parameter name to match route
    if location_id not in weather_data:
        return jsonify({"error": "Location not found"}), 404

    location_weather = weather_data[location_id]
    if not location_weather:
        return jsonify({"error": "No weather data available for this location"}), 404

    # No date provided - return latest forecast
    if not dt_input:
        latest_date = max(location_weather.keys())
        return (
            jsonify(
                {
                    "location_id": location_id,
                    "datetime": latest_date.isoformat(),
                    "weather": location_weather[latest_date],
                }
            ),
            200,
        )

    try:
        # Date without time (YYYY-MM-DD)
        if "T" not in dt_input:
            dt_input = dt_input + "T00:00:00"
            target_date = datetime.fromisoformat(dt_input)

            # Get all timestamps for that date
            same_day_forecasts = [
                dt for dt in location_weather.keys() if dt.date() == target_date.date()
            ]

            if not same_day_forecasts:
                return jsonify({"error": "No weather data for specified date"}), 404

            # Return the latest forecast for that date
            latest_time = max(same_day_forecasts)
            return (
                jsonify(
                    {
                        "location_id": location_id,
                        "datetime": latest_time.isoformat(),
                        "weather": location_weather[latest_time],
                    }
                ),
                200,
            )

        # Specific datetime
        target_date = datetime.fromisoformat(dt_input)
        weather = location_weather.get(target_date)
        if weather is None:
            return jsonify({"error": "No weather data for specified datetime"}), 404

        return (
            jsonify(
                {"location_id": location_id, "datetime": dt_input, "weather": weather}
            ),
            200,
        )

    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400


if __name__ == "__main__":
    app.run(port=5002, debug=True)
