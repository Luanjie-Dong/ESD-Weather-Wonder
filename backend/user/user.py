from flask import Flask, request, jsonify
import os
from supabase import AuthApiError, create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SUPER_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)

@app.route("/signin", methods=["POST"])
def signin():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        response = supabase.auth.sign_in_with_password(
            {
            "email": email,
            "password": password
            }
        )

        #user = response.user
        #identities = user.identities if user and hasattr(user, "identities") else []
        #user_id = identities[0].id if identities else None

        return jsonify({
            "code": 200,
            "message": "Sign in successful"
            #"user": [dict(identity) for identity in identities],  # Ensure identities are serializable
            #"user_id": user_id
        }), 200
    
    except ValueError as ve:
        return jsonify({
            {"code": 400,
            "message": str(ve)}
        }), 400
    
    except AuthApiError as aae:
        return jsonify({
            "code": 401,
            "message": str(aae)
        }), 401
    
    except Exception as e:
        return jsonify({
            {"code": 500,
            "message": str(e)}
        }), 500


@app.route("/signout", methods=['POST'])
def signout():
    try:
        response = supabase.auth.sign_out()
        return jsonify({
            "code": 200,
            "message": "Successfully signed out."
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Error: " + str(e)
        }), 500

    
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
            "data": response.model_dump() if response else None
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

        response = supabase.auth.sign_up(
            {
                "email": email, 
                "password": password,
            }
        )

        user = response.user
        session = response.session

        user_id = str(user.id)
        signin()

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


@app.route("/users/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])
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
                "message": "Not signed in."
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
        country = data.get("country")
        state = data.get("state")
        city = data.get("city")

        response = supabase.table("user").update({"username": username, "email": email, 
                                                      "country": country, "state": state, "city": city}).eq("user_id", user_id).execute()

        supabase.auth.admin.update_user_by_id(user_id,
            {
                "email": email,
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



@app.route("/user", methods=['GET', 'PUT', 'DELETE'])
def user_operations():
    if request.method == 'PUT':
        return update_user()
    elif request.method == 'DELETE':
        return delete_user()
    elif request.method == 'GET':
        return get_user()
    
def get_user():
    """
    Retrieves current signed in user's details.
    """
    try:
        response = supabase.auth.get_user()
        
        if response:
            user_id = response.user.id
            response = supabase.table("user").select("*").eq("user_id", user_id).execute()
            user = response.data

            return jsonify({
                "code": 201,
                "user": user[0] if user else None
            }), 201
        else:
            return jsonify({
                "code": 401,
                "message": "Not signed in."
            }), 401
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500
    
def update_user():
    try:
        user, status = get_user()

        if status == 201:
            user_id = user.get_json().get("user", {}).get("user_id")
            
            data = request.get_json()
            username = data.get("username")
            email = data.get("email")
            country = data.get("country")
            state = data.get("state")
            city = data.get("city")

            response = supabase.table("user").update({"username": username, "email": email, 
                                                      "country": country, "state": state, "city": city}).eq("user_id", user_id).execute()


            return jsonify({
                "code": 200,
                "message": "User successfully updated.",
                "user": response.data[0]
            }), 200
        
        elif status == 401:
            return jsonify({
                "code": 401,
                "Error": user.get_json()
            }), 401

        return
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500

def delete_user():
    try:
        user, status = get_user()

        if status == 201:
            user_id = user.get_json().get("user", {}).get("user_id")
            response = supabase.table("user").delete().eq("user_id", user_id).execute()
            supabase.auth.admin.delete_user(user_id)

            return jsonify({
                "code": 200,
                "message": "User successfully deleted."
            }), 200
        
        elif status == 401:
            return jsonify({
                "code": 401,
                "Error": user.get_json()
            }), 401

        return
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)