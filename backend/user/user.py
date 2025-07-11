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
admin_key: str = os.environ.get("SUPABASE_SUPER_KEY")

supabaseAdmin: Client = create_client(url, admin_key)
supabase: Client = create_client(url, key)


app = Flask(__name__)
CORS(app)
  
@app.route("/all-users")
def get_users():
    try:
        response = (
            supabaseAdmin.table("user")
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
        response = supabaseAdmin.rpc("get_user_emails", {"user_ids": user_ids}).execute()
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
        response = supabaseAdmin.rpc("get_emails_by_location").execute()
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


@app.route("/reset_password/<string:user_id>", methods=['PUT'])
def change_password(user_id):
    try:
        data = request.get_json()
        password = data.get("password")

        supabaseAdmin.auth.admin.update_user_by_id(user_id, {
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
    try:
        response = supabaseAdmin.table("user").select("*").eq("user_id", user_id).execute()
        
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

def update_user_by_route(user_id):
    try:
        res = supabaseAdmin.table("user").select("*").eq("user_id", user_id).execute()
        user = res.data[0]

        data = request.get_json()
        username = data.get("username", user['username'])
        email = data.get("email", user['email'])
        password = data.get("password") # no way to retrieve password individually from Auth side
        country = data.get("country", user['country'])
        state = data.get("state", user['state'])
        city = data.get("city", user['city'])
        neighbourhood = data.get("neighbourhood", user['neighbourhood'])

        response = supabaseAdmin.table("user").update({"username": username, "email": email, 
                                                      "country": country, "state": state, "city": city, "neighbourhood": neighbourhood}).eq("user_id", user_id).execute()

        # Ensures that no ill entries are entered
        if email and password:
            supabaseAdmin.auth.admin.update_user_by_id(user_id,
                {
                    "email": email,
                    "password": password
                }
            )

        if email:
             supabaseAdmin.auth.admin.update_user_by_id(user_id,
                {
                    "email": email
                }
            )

        if password:
             supabaseAdmin.auth.admin.update_user_by_id(user_id,
                {
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
        response = supabaseAdmin.table("user").delete().eq("user_id", user_id).execute()
        response = supabaseAdmin.auth.admin.delete_user(user_id)

        return jsonify({
            "code": 200,
            "message": "User successfully deleted."
        }), 200
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Error: {e}"
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
        neighbourhood = data.get("neighbourhood")

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
            .insert({"user_id": user_id, "email": email, "username": username, "country": country, "state": state, "city": city, "neighbourhood": neighbourhood})
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
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; background-color: #f0f8ff; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <h2 style="color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 20px; color: #3498db;">
                        Welcome, {user['username']}!
                    </h2>
                    <p style="font-size: 16px; margin-bottom: 10px;">
                        <strong>Thank you for signing up with WeatherWonder!</strong>
                    </p>
                    <p style="font-size: 16px; margin-bottom: 10px;">
                        We've successfully registered your account with the following details:
                    </p>
                    <ul style="font-size: 16px; margin-bottom: 20px; list-style: none; padding: 0;">
                        <li><strong>Email:</strong> {user['email']}</li>
                        <li><strong>Location:</strong> {user['neighbourhood']}, {user['city']}, {user['country']}</li>
                        <li><strong>Username:</strong> {user['username']}</li>
                    </ul>
                    <p style="font-size: 16px; margin-bottom: 10px;">
                        You'll start receiving daily weather forecasts soon.
                    </p>
                    <p style="font-size: 16px; margin-bottom: 10px;">
                        If you have any questions, feel free to reach out to our support team.
                    </p>
                    <br>
                    <p style="font-size: 14px; color: #777;">
                        Cheers,<br>The WeatherWonder Team
                    </p>
                    <footer style="margin-top: 30px; font-size: 14px; color: #3498db;">
                        <p>WeatherWonder - Your trusted weather partner</p>
                    </footer>
                </div>
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)