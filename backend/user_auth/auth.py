from flask import Flask, request, jsonify
import os
import pika
import json
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

        response = supabase.auth.sign_up(
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

@app.route("/signinstatus", methods=["POST"])
def sign_in_status():
    try:
        response = supabase.auth.get_user()

        if response:
            return jsonify({
                "code": 200,
                "user_id": response.user.id
            }), 200
        else:
            return jsonify({
                "code": 401,
                "message": "You are not signed in."
            }), 401

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500

@app.route("/signout", methods=["POST"])
def signout():
    """
    Signs out the user by invalidating their current session.

    This function handles the logout process by revoking the user's session in Supabase Auth,
    which effectively signs the user out from the application. After a successful signout, 
    the user is logged out and the client can no longer perform authenticated actions without 
    signing in again.

    Returns:
    JSON response:
        - On success: Returns a message confirming the user has been signed out with a status code of 200.
        - On failure: Returns an error message and a status code of 500.
    
    Example:
    Request: POST /signout
    Response: {"code": 200, "message": "User successfully signed out."}
    """
    try:
        supabase.auth.sign_out()

        return jsonify({
            "code": 200,
            "message": "User successfully signed out."
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Error: {str(e)}"
        }), 500


@app.route("/signin", methods=["POST"])
def sign_in_user():
    """
    Sign-in a user using their email and password.
    
    This function uses Supabase Auth to authenticate a user based on their email and password.
    If authentication is successful, it returns the user's data (user_id, email, etc.) and a session token.
    If authentication fails (wrong credentials), it returns an error message.
    
    Raises:
        Exception: If login fails due to invalid credentials or service unavailability.
    """
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        response = supabase.auth.sign_in_with_password(
            {
                "email": email, 
                "password": password,
            }
        )

        if response.user:

            response = supabase.table("user").select("*").eq("user_id", response.user.id).execute()
            
            if response:
                user = response.data

                return jsonify({
                    "code": 201 if user else 404,
                    "message": "User signed in successfully.",
                    "user": user[0] if user else None
                }), 201 if user else 404
            else:
                return jsonify({
                    "code": 401,
                    "message": "Not found"
                }), 401

        else:
            return jsonify({
                "code": 401,
                "message": "Invalid email or password."
            }), 401
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Error: {str(e)}"
        }), 500
    
@app.route("/reset_password", methods=['PUT'])
def change_password():
    response, status = sign_in_status()
    data = response.get_json()
    user_id = data.get("user_id")
    if status == 200:
        try:
            data = request.get_json()
            password = data.get("password")

            supabase.auth.update_user(
            {
                "password": password
            })
            return jsonify({
                "message": "User password successfully changed."
            })
        except Exception as e:
            return jsonify({
                "message": str(e)
            })
    else:
        return jsonify({
            "code": 401,
            "message": "You are not signed in"
        }), 401

@app.route("/user_email/<string:email>")
def getuserbyemail(email):
    """
    Retrieves the user details for the specified email address from the Supabase database.

    This route queries the 'user' table in the Supabase database to find a user based on the provided 
    email. If the user exists and valid data is returned (i.e., not null or empty), it returns the 
    user's details. Otherwise, it returns an error message indicating that the user was not found.

    Parameters:
    email (string): The email address of the user to be retrieved.

    Returns:
    JSON response:
        - On success (found user): Returns a JSON object with the user's details and a status code of 201.
        - On failure (user not found): Returns a JSON object with user as null and a status code of 404.
        - On error: Returns a JSON object with the error message and a status code of 500.

    Example:
    Request: GET /user_email/test1@example.com
    Response: {"code": 201, "user": {"email": "test1@example.com", "username": "TestUser", "city": "Singapore"}}
    """
    response, status = sign_in_status()
    if status == 200:
        try:
            response = supabase.table("user").select("*").eq("email", email).execute()
            
            if response:
                user = response.data

                return jsonify({
                    "code": 201 if user else 404,
                    "user": user[0] if user else None
                }), 201 if user else 404
            else:
                return jsonify({
                    "code": 404,
                    "message": "User not found."
                }), 404
        
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 500
    else:
        return jsonify({
            "code": 401,
            "message": "You are not signed in"
        }), 401

    
@app.route("/user", methods=['GET', 'PUT'])
def user_operations_route():
    if request.method == 'PUT':
        return updateuser()
    elif request.method == 'GET':
        return getuser()

def getuser():
    """
    Retrieves the user details for the specified user_id from the Supabase database.

    This route queries the 'user' table in the Supabase database to find a user based on the provided 
    user_id. If the user exists and valid data is returned (i.e., not null or empty), it returns the 
    user's details. Otherwise, it returns an error message indicating that the user was not found.

    Parameters:
    user_id (string): The unique identifier (user_id) of the user to be retrieved.

    Returns:
    JSON response:
        - On success (found user): Returns a JSON object with the user's details and a status code of 201.
        - On failure (user not found): Returns a JSON object with user as null and a status code of 404.
        - On error: Returns a JSON object with the error message and a status code of 500.

    Example:
    Request: GET /user_id/22ae7899-3529-40b3-b03d-d727443bf68a
    Response: {"code": 201, "user": {"user_id": "22ae7899-3529-40b3-b03d-d727443bf68a", "username": "TestUser", "city": "Singapore"}}
    """
    response, status = sign_in_status()
    data = response.get_json()
    user_id = data.get("user_id")
    if status == 200:
        try:
            response = supabase.table("user").select("*").eq("user_id", user_id).execute()
            
            if response:
                user = response.data

                return jsonify({
                    "code": 201 if user else 404,
                    "user": user[0] if user else None
                }), 201 if user else 404
            else:
                return jsonify({
                    "code": 401,
                    "message": "Not found"
                }), 401
        
        except Exception as e:
            return jsonify({
                "message": str(e)
            }), 500
    else:
        return jsonify({
            "code": 401,
            "message": "You are not signed in"
        }), 401

def updateuser():
    response, status = sign_in_status()
    data = response.get_json()
    user_id = data.get("user_id")
    if status == 200:
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

            supabase.auth.update_user(
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
    else:
        return jsonify({
            "code": 401,
            "message": "You are not signed in"
        }), 401



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)