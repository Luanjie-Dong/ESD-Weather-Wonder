import pika
import json
import os

# Set these according to your .env or docker-compose settings
RABBITMQ_HOST = os.getenv("AMQP_HOST", "localhost")  # or "rabbitmq" if inside Docker
RABBITMQ_PORT = int(os.getenv("AMQP_PORT", 5672))
USERNAME = os.getenv("AMQP_USER", "myuser")
PASSWORD = os.getenv("AMQP_PASS", "secret")

EXCHANGE_NAME = "esd_weatherwonder"
ROUTING_KEY = "location.weather.update"  # matches "#.update"

message = {
    "datetime": "2025-03-05T12:00:00",
    "location_id": "abc123",
    "weather": {
        "description": "partly cloudy",
        "feels_like": 32.1,
        "humidity": 85,
        "temp": 28.5,
        "wind_speed": 3.5
    }
}

message_2 = {
    "location_id": "abc123",
    "forecast_day": "2025-03-25",
    "poll_datetime": "2025-03-25 08:00:00",
    "hourlyForecast": [
        {
            "time": "2025-03-25 08:00",
            "temp_c": 22.5,
            "condition_text": "Partly Cloudy",
            "condition_icon": "partly_cloudy_icon.png",
            "wind_kph": 10.5,
            "precip_mm": 0.0,
            "humidity": 85
        }
    ]
}


message_new = {
  "forecast_day": "2025-03-22",
  "hourly_forecast": [
    {
      "time": "14:00",
      "temp_c": 28.3,
      "condition_text": "Partly Cloudy",
      "condition_icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
      "wind_kph": 10.5,
      "precip_mm": 0.0,
      "humidity": 65
    }
  ]
}
  

# Connect to RabbitMQ
credentials = pika.PlainCredentials(USERNAME, PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
)
channel = connection.channel()

# Declare exchange (should already exist)
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

# Publish message
channel.basic_publish(
    exchange=EXCHANGE_NAME,
    routing_key=ROUTING_KEY,
    body=json.dumps(message_2),
    properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
)

print(f"✅ Sent test message to {EXCHANGE_NAME} with routing key '{ROUTING_KEY}'")

connection.close()
