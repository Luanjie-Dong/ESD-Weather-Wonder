from flask import Flask, request, jsonify
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)

  
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
    Registers user into Supabase Auth and DB
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