import json
from flask import Flask, request, jsonify
import os
import pika
from supabase import create_client, Client
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

RABBITMQ_HOST = os.getenv("AMQP_HOST")
RABBITMQ_PORT = int(os.getenv("AMQP_PORT"))
USERNAME = os.getenv("AMQP_USER")
PASSWORD = os.getenv("AMQP_PASS")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)
  
@app.route("/all-users")
def get_users():
    try:
        response = (
            supabase.table("user")
            .select("*")
            .execute()
        )
        return jsonify({
            "code": 201,
            "count": len([key for key in response.data]),
            "users": response.data
        }), 201
        
    except Exception as e:
        print("Supabase Error:", e)
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500

@app.route("/get-user-emails")
# RPC Call for custom SQL query on User table in Supabase
def get_user_emails():
    '''Performs RPC Call to retrieve emails of all user ids sent in. Accepts an array of user_ids'''
    try:
        data = request.get_json()
        user_ids = data.get("user_ids")
        response = supabase.rpc("get_user_emails", {"user_ids": user_ids}).execute()
        print(type(response))
        return jsonify({
            "code": 201,
            "count": len(response.data),
            "emails_by_location": response.data
        }), 201
        
    except Exception as e:
        print("Supabase Error:", e)
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500

@app.route("/emails-by-location")
# RPC Call for custom SQL query on User table in Supabase
def get_emails_by_location():
    try:
        response = supabase.rpc("get_emails_by_location").execute()
        print(type(response))
        return jsonify({
            "code": 201,
            "count": len(response.data),
            "emails_by_location": response.data
        }), 201
        
    except Exception as e:
        print("Supabase Error:", e)
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500

@app.route("/signup", methods=['POST'])
def register_user():
    """
    Registers a new user in both Supabase Auth and the application database.

    This function creates a new user account using Supabase's authentication service,
    and also stores user-related metadata (e.g., email, username) in a separate
    user profile table within the Supabase database.

    Raises:
        Exception: If user registration fails due to invalid input, duplicate accounts, 
        or service unavailability.
    """
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        username = data.get("username")
        country = data.get("country")
        state = data.get("state")
        city = data.get("city")

        response = supabase.auth.admin.create_user(
            {
                "email": email,
                "password": password
            }
        )

        user = response.user

        user_id = str(user.id)

        response = (
            supabase.table("user")
            .insert({"user_id": user_id, "email": email, "username": username, "country": country, "state": state, "city": city})
            .execute()
        )

        publishUserNotification(response.data[0])
            
        return jsonify(
            {
                "code": 201,
                "message": "User successfully created",
                "user": response.data[0]
            }
        ), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify(
            {
            "code": 500,
            "message": str(e)
            }

        ), 500
    
def publishUserNotification(user):
    """Publishes a message through
    RabbitMQ to Notification Queue with routing key 'user.notification'
    """
    ROUTING_KEY = "user.notification"
    QUEUE = "Notification"

    subject = "Welcome to WeatherWonder!"
    content = f"""
        <html>
            <body>
                <h2>Welcome, {user['username']}!</h2>
                <p>Thank you for signing up with WeatherWonder.</p>
                <p>We've registered your account with the following details:</p>
                <ul>
                    <li>Email: {user['email']}</li>
                    <li>Location: {user['city']}, {user['country']}</li>
                    <li>Username: {user['username']}</li>
                </ul>
                <p>You'll start receiving daily weather forecasts soon.</p>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <br>
                <p>Cheers,<br>The WeatherWonder Team</p>
            </body>
        </html>
    """
    msg = {
        "recipients": user["email"],
        "subject": subject,
        "content": content,
        "bcc": False                    
    }


    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

    channel.queue_declare(queue=QUEUE, durable=True, arguments={"x-max-priority": 10})
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE, routing_key=ROUTING_KEY) 

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY,
        body=json.dumps(msg),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    print(f"✅ Sent test message to {EXCHANGE_NAME} with routing key '{ROUTING_KEY}'")

    connection.close()

    return
    
@app.route("/reset_password/<string:user_id>", methods=['PUT'])
def change_password(user_id):
    try:
        data = request.get_json()
        password = data.get("password")

        supabase.auth.admin.update_user_by_id(user_id, {
            "password": password
        })
        return jsonify({
            "message": "User password successfully changed."
        })
    except Exception as e:
        return jsonify({
            "message": str(e)
        })


@app.route("/user/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
def user_operations_route(user_id):
    if request.method == 'PUT':
        return update_user_by_route(user_id)
    elif request.method == 'DELETE':
        return delete_user_by_route(user_id)
    elif request.method == 'GET':
        return get_user_by_route(user_id)

def get_user_by_route(user_id):
    """
    Retrieves current signed in user's details.
    """
    try:
        response = supabase.table("user").select("*").eq("user_id", user_id).execute()
        
        if response:
            user = response.data

            return jsonify({
                "code": 201,
                "user": user[0] if user else None
            }), 201
        else:
            return jsonify({
                "code": 401,
                "message": "Not found"
            }), 401
    
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500

def update_user_by_route(user_id):
    try:            
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        country = data.get("country")
        state = data.get("state")
        city = data.get("city")

        response = supabase.table("user").update({"username": username, "email": email, 
                                                      "country": country, "state": state, "city": city}).eq("user_id", user_id).execute()

        supabase.auth.admin.update_user_by_id(user_id,
            {
                "email": email,
                "password": password
            }
        )

        return jsonify({
            "code": 200,
            "message": "User successfully updated.",
            "user": response.data[0]
        }), 200
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500

def delete_user_by_route(user_id):
    try:
        response = supabase.table("user").delete().eq("user_id", user_id).execute()
        response = supabase.auth.admin.delete_user(user_id)

        return jsonify({
            "code": 200,
            "message": "User successfully deleted."
        }), 200
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Error: {e}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)