from flask import Flask, request, jsonify
import os
import json
import threading
import requests
from dotenv import load_dotenv
import amqp_lib

load_dotenv()

app = Flask(__name__)

# ENV Configs
USER_URL = os.getenv("USER_URL")
USERLOCATION_URL = os.getenv("USERLOCATION_URL")
AMQP_HOST = os.getenv("AMQP_HOST", "localhost")
AMQP_PORT = int(os.getenv("AMQP_PORT", 5672))
AMQP_USER = os.getenv("AMQP_USER")
AMQP_PASS = os.getenv("AMQP_PASS")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "esd_weatherwonder")
EXCHANGE_TYPE = os.getenv("EXCHANGE_TYPE", "topic")
QUEUE_NAME = "Trigger_Forecast_Process"
PUBLISHER_QUEUE_NAME = "Notification"
PUBLISHER_ROUTING_KEY = "weather.forecast.notification"
SUBSCRIBER_ROUTING_KEY = "#.update"
queue_arguments={"x-max-priority": 10}


# Shared channel for publishing
channel = None

def subscriber_callback(ch, method, properties, body):
    message_str = body.decode()
    try:
        message_json = json.loads(message_str)
        print(f" [X] Received: {json.dumps(message_json, indent=4)}")
        processLocationWeather(message_json)
    except Exception as e:
        print(f"Failed to process message: {e}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def processLocationWeather(body):
    location_id = body['location_id']
    print(f" [x] Processing location Id: {location_id}")

    userlocation_resp = queryUserLocations(location_id)
    if not userlocation_resp:
        print("No users found for location")
        return

    emails = queryUserEmails(userlocation_resp)
    if not emails:
        print("No emails returned")
        return

    print(f"Publishing Email List: {emails}")
    publishMessage(emails, body['weather'])


def queryUserLocations(location_id):
    try:
        url = f"{USERLOCATION_URL}/UserLocation/rest/v1/GetUserLocations/location/{location_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "ErrorMessage" not in data.get("Result", {}):
            return data.get("UserLocations", [])
        else:
            print("Error:", data["Result"]["ErrorMessage"])
    except requests.RequestException as e:
        print(f"API error: {e}")
    return None


def queryUserEmails(userlocation):
    user_ids = {"user_ids": [user["UserId"] for user in userlocation]}
    try:
        response = requests.get(f"{USER_URL}/get-user-emails", json=user_ids, timeout=5)
        response.raise_for_status()
        users_rpc = response.json()
        return [user["email"] for user in users_rpc.get("emails_by_location", [])]
    except requests.RequestException as e:
        print(f"Email fetch error: {e}")
    return None


def publishMessage(emails, weather):
    global channel
    if not channel:
        print("No channel available for publishing.")
        return

    # Publish to Notification
    channel.queue_declare(queue=PUBLISHER_QUEUE_NAME, durable=True, arguments={"x-max-priority": 10})
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=PUBLISHER_QUEUE_NAME, routing_key=PUBLISHER_ROUTING_KEY) 
    
    for email in emails:
        content = f"{weather['description']}, temperature: {weather['temp']}°C, feels like {weather['feels_like']}°C, wind speed: {weather['wind_speed']}km/h, humidity: {weather['humidity']}%"
        print("CONTENT:",content)
        msg = {
            "recipients": email,
            "subject": "DAILY WEATHER FORECAST",
            "content": content,
            "bcc": False                    
        }


        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=PUBLISHER_ROUTING_KEY,
            body=json.dumps(msg),
            properties=amqp_lib.pika.BasicProperties(delivery_mode=2)
        )


def setup_consumer():
    global channel
    connection, channel_ = amqp_lib.connect(
        hostname=AMQP_HOST,
        port=AMQP_PORT,
        exchange_name=EXCHANGE_NAME,
        exchange_type=EXCHANGE_TYPE,
        username=AMQP_USER,
        password=AMQP_PASS
    )
    channel = channel_

    print(f"Starting consumer on {QUEUE_NAME}...")
    amqp_lib.start_consuming(
        hostname=AMQP_HOST,
        port=AMQP_PORT,
        exchange_name=EXCHANGE_NAME,
        exchange_type=EXCHANGE_TYPE,
        queue_name=QUEUE_NAME,
        callback=subscriber_callback,
        username=AMQP_USER,
        password=AMQP_PASS,
        routing_key=SUBSCRIBER_ROUTING_KEY,
        queue_arguments=queue_arguments
    )


if __name__ == '__main__':
    # Start consumer thread
    threading.Thread(target=setup_consumer, daemon=True).start()
    app.run(host='0.0.0.0', port=5020, debug=True)
