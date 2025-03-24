# Poll Weather Forecast Service

This microservice is responsible for polling weather forecasts for all registered locations on a daily basis. It interacts with several other microservices to provide weather forecast data.

## Service Dependencies

### Location Service
- **URL**: `LOCATION_URL` (default: http://location:5002)
- **Endpoint**: GET /locations
- **Response Schema**:
  ```json
  [
    {
      "location_id": "string",
      "country": "string",
      "state": "string",
      "city": "string",
      "neighbourhood": "string"
    }
  ]
  ```

### Weather Service
- **URL**: `WEATHER_URL` (default: http://weather:8081)
- **Endpoint**: POST /graphql
- **Request Schema**:
  ```graphql
  query GetForecast($country: String!, $state: String!, $city: String!, $neighbourhood: String!) {
    getForecast {
      location { name, region, country, localtime }
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
  ```

### Location Weather Service
- **URL**: `LOCATION_WEATHER_URL` (default: http://location_weather:5003)
- **Endpoint**: POST /update_forecast/{location_id}
- **Request Schema**:
  ```json
  {
    "forecast_day": "string (YYYY-MM-DD)",
    "hourly_forecast": [
      {
          "time": "YYYY-MM-DD HH:MM",
          "temp_c": "number",
          "condition_text": "string",
          "condition_icon": "string",
          "wind_kph": "number",
          "precip_mm": "number",
          "humidity": "number",
          "will_it_rain": "number",
          "chance_of_rain": "number",
          "will_it_rain": "number",
          "chance_of_rain": "number"
      }
    ]
  }
  ```

## API Endpoints

### Home Endpoint
- **Method**: GET
- **Path**: /
- **Response**: String indicating service status

### Health Check
- **Method**: GET
- **Path**: /health
- **Response Schema**:
  ```json
  {
    "status": "string",
    "services": {
      "location": "boolean",
      "weather": "boolean",
      "location_weather": "boolean"
    }
  }
  ```

### Trigger Poll (`curl +X POST localhost:5005/trigger-poll` to manually trigger and poll)
- **Method**: POST
- **Path**: /trigger-poll
- **Response Schema**:
  ```json
  {
    "timestamp": "string (ISO format)",
    "locations_processed": "number",
    "results": [
      {
        "location_id": "string",
        "status": "string (success/failed)",
        "location": "string",
        "error": "string (optional)"
      }
    ]
  }
  ```

## Scheduling

The service automatically polls weather forecasts at midnight (00:00) every day. The scheduling is handled by the Python `schedule` library and runs in a separate thread.

## Running the Service

### Environment Variables
Make sure to set the following environment variables:
- `LOCATION_URL`: URL of the location service
- `WEATHER_URL`: URL of the weather service
- `LOCATION_WEATHER_URL`: URL of the location_weather service

### Start the Service
```bash
python poll_weather_forecast.py
```

The service will start on port 5005 by default.