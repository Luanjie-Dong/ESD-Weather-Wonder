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

    userlocations = queryUserLocations(location_id)
    if not userlocations:
        print("No users found for location")
        return

    users = queryUserEmails(userlocations)
    if not users:
        print("No emails returned")
        return
    
    full_package_users = packageEmailLocation(users, userlocations)

    print(f"Publishing Email List: {users}")
    publishMessage(full_package_users, body['hourlyForecast'])

def packageEmailLocation(users, userlocations):
    result = []
    for user in users:
        userid = user["user_id"]
        email = user["email"]
        for location in userlocations:
            if location["UserId"] == userid:
                result.append({
                    "userid": userid,
                    "email": email,
                    "label": location["Label"],
                    "address": location["Address"]
                })

    return result


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

        return [user for user in users_rpc.get("emails_by_location", [])]
    except requests.RequestException as e:
        print(f"Email fetch error: {e}")
    return None


def publishMessage(users, weather):
    global channel
    if not channel:
        print("No channel available for publishing.")
        return

    # Publish to Notification
    channel.queue_declare(queue=PUBLISHER_QUEUE_NAME, durable=True, arguments={"x-max-priority": 10})
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=PUBLISHER_QUEUE_NAME, routing_key=PUBLISHER_ROUTING_KEY) 

    forecast = weather[0]

    for user in users:
        content = f"""
        <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; background-color: #f9f9f9; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <h2 style="color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 20px;">
                        Daily Weather Forecast – {user["label"]}
                    </h2>
                    <p style="font-size: 16px; margin-bottom: 10px;">
                        <strong>Location:</strong> {user["address"]}
                    </p>
                    <p style="font-size: 16px; margin-bottom: 10px;">
                        <strong>Condition:</strong> {forecast['condition_text']}<br>
                        <img src="https:{forecast['condition_icon']}" alt="Weather Icon" style="width: 50px; height: 50px;"/>
                    </p>
                    <p style="font-size: 16px; margin-bottom: 10px;">
                        <strong>Temperature:</strong> {forecast['temp_c']}°C<br>
                    </p>
                    <table style="width: 100%; font-size: 16px; border-collapse: collapse; margin-top: 20px;">
                        <tr>
                            <td style="padding: 8px 0;"><strong>Wind Speed:</strong></td>
                            <td style="text-align: right;">{forecast['wind_kph']} km/h</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Humidity:</strong></td>
                            <td style="text-align: right;">{forecast['humidity']}%</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Precipitation:</strong></td>
                            <td style="text-align: right;">{forecast['precip_mm']} mm</td>
                        </tr>
                    </table>
                    <p style="font-size: 14px; color: #777; margin-top: 30px;">
                        Stay safe and plan your day accordingly.
                    </p>
                </div>
            </body>
        </html>
        """
        
        subject = f"DAILY WEATHER FORECAST : {user['label']}"

        msg = {
            "recipients": user["email"],
            "subject": subject,
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
