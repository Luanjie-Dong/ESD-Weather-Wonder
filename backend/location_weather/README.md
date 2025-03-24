# Location Weather Service
This service provides weather forecast data for specific locations. It runs on port 5003 and interacts with a Supabase database to store and retrieve weather forecasts.

## Quick Setup 

### Local Deployment
#### Running the project directly
1. Create your own supabase table and schema, then update your `.env` file with your credentials
```bash
SUPABASE_URL = YOUR_SUPABASE_DB_URL
SUPABASE_KEY = YOUR_SUPABASE_API_KEY
```
2. Requirements 
```bash
pip install -r requirements.txt
```
3. Run
```bash
python main.py
```

#### Building docker image
1. Docker Build
```bash
docker build -t location_weather .
```
2. Docker Run
```bash
docker run -p 5003:5003 --env-file .env location_weather
```

## API Endpoints

### 1. Get Latest Weather Forecast
Returns the latest 24-hour weather forecast for a specific location.

- **Method**: GET
- **Path**: `/get_weather/<location_id>`
- **Response**:
```json
{
    "location_id": "string",
    "forecast_day": "YYYY-MM-DD",
    "poll_datetime": "YYYY-MM-DD HH:MM:SS",
    "hourlyForecast": [
        {
            "time": "YYYY-MM-DD HH:MM",
            "time_epoch": "number",
            "temp_c": "number",
            "condition_text": "string",
            "condition_icon": "string",
            "condition_code": "number",
            "wind_kph": "number",
            "wind_degree": "number",
            "wind_dir": "string",
            "pressure_mb": "number",
            "precip_mm": "number",
            "humidity": "number",
            "cloud": "number",
            "feelslike_c": "number",
            "windchill_c": "number",
            "heatindex_c": "number",
            "dewpoint_c": "number",
            "will_it_rain": "number",
            "chance_of_rain": "number",
            "will_it_snow": "number",
            "chance_of_snow": "number",
            "vis_km": "number",
            "gust_kph": "number",
            "uv": "number"
        }
    ]
}
```

### 2. Get Weather Forecast by Date
Returns all weather forecasts for a specific date.

- **Method**: GET
- **Path**: `/get_weather/date/<location_id>/<date>`
- **Parameters**:
  - `date`: Format YYYY-MM-DD
- **Response**:
```json
{
    "location_id": "string",
    "forecast_day": "YYYY-MM-DD",
    "poll_datetime": "YYYY-MM-DD HH:MM:SS",
    "hourlyForecast": [
        {
            "time": "YYYY-MM-DD HH:MM",
            "time_epoch": "number",
            "temp_c": "number",
            "condition_text": "string",
            "condition_icon": "string",
            "condition_code": "number",
            "wind_kph": "number",
            "wind_degree": "number",
            "wind_dir": "string",
            "pressure_mb": "number",
            "precip_mm": "number",
            "humidity": "number",
            "cloud": "number",
            "feelslike_c": "number",
            "windchill_c": "number",
            "heatindex_c": "number",
            "dewpoint_c": "number",
            "will_it_rain": "number",
            "chance_of_rain": "number",
            "will_it_snow": "number",
            "chance_of_snow": "number",
            "vis_km": "number",
            "gust_kph": "number",
            "uv": "number"
        }
    ]
}
```

### 3. Get Weather Forecast by DateTime
Returns the weather forecast for a specific hour.

- **Method**: GET
- **Path**: `/get_weather/datetime/<location_id>/<dt_input>`
- **Parameters**:
  - `dt_input`: Format YYYY-MM-DD HH:MM:SS
- **Response**:
```json
{
    "location_id": "string",
    "forecast_day": "YYYY-MM-DD",
    "weather": {
        "time": "YYYY-MM-DD HH:MM",
        "temp_c": "number",
        "condition_text": "string",
        "condition_icon": "string",
        "wind_kph": "number",
        "precip_mm": "number",
        "humidity": "number",
        "will_it_rain": "number",
        "chance_of_rain": "number"
    }
}
```

### 4. Update Weather Forecast
Inserts a new 24-hour forecast into the database.

- **Method**: POST
- **Path**: `/update_forecast/<location_id>`
- **Request Body**:
```json
{
    "forecast_day": "YYYY-MM-DD",
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
            "chance_of_rain": "number"
        }
    ]
}
```
- **Response**:
```json
{
    "message": "Weather forecast updated successfully"
}
```

## Database Schema
The service uses a Supabase table with the following structure:

**Table**: `location_weather`
- `location_id` (Primary Key): integer
- `poll_datetime` (Primary Key): datetime (auto-inserted using now())
- `hourly_forecast`: json (24h forecast)
- `forecast_day`: date (local forecast date)

## Service Dependencies
### Location Service
- **URL**: `LOCATION_SERVICE_URL` (default: http://location:5002)
- Used for validating location IDs before processing weather data

## Authentication
1. Generate JWT Secret with OpenSSL
```bash
openssl random -base64 256
```
2. Update `.env` file with JWT Secret
```bash
JWT_SECRET = YOUR_JWT_SECRET
```
3. Share your JWT Secret with the other services that depend on you and call them
4. Remember to also add in your service URL, then use this in your code to call the desired MS to make it dynamic
```bash
MICROSERVICE_URL = SERVICES_WHO_WILL_CALL_YOUR_MS_URL
```