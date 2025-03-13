from flask import Flask, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
#from clerk_backend_api import Clerk

import requests
import os

# Load environment variables
load_dotenv()

# Flask App
app = Flask(__name__)

# Clerk API Key
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_BASE_URL = "https://api.clerk.dev/v1"
#clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))


# Supabase Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Headers for Clerk API
HEADERS = {
    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
    "Content-Type": "application/json"
}

@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        username = data.get("username")
        country = data.get("country")
        state = data.get("state")
        city = data.get("city")

        clerk_response = requests.post(
            f"{CLERK_BASE_URL}/users",
            json={"email_address": [email], "password": password},
            headers=HEADERS
        )
        clerk_data = clerk_response.json()

        if clerk_response.status_code != 200:
            return jsonify({"error": "Clerk signup failed", "details": clerk_data}), clerk_response.status_code

        clerk_user_id = clerk_data.get("id")

        supabase_response = supabase.table("user").insert({"user_id": clerk_user_id, "email": email, "username": username,
                                                           "country": country, "state": state, "city": city}).execute()

        return jsonify({"message": "User created successfully","supabase": supabase_response.data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/signin", methods=["POST"])
def signin():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        user_id = get_user_id_by_email(email)

        if user_id:
            try:
                resp_valid = verify_password(user_id, password)
                
                if resp_valid == False:
                    return {"message": "Incorrect password entered"}, 401

                resp_session = create_session(user_id)

            except Exception as e:
                return jsonify({
                    "message": str(e)
                }), 500
        else:
            return jsonify({
                "message": "Email not found"
            }), 400

        return jsonify({
            "message": "Login successful",
            "session info": {
                "user_id": resp_session['user_id'],
                "session_token": resp_session['id']
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_user_id_by_email(email):
    response = requests.get(
        f"{CLERK_BASE_URL}/users",
        params={"email_address": email},
        headers=HEADERS
    )

    data = response.json()
    if response.status_code == 200 and len(data) > 0:
        return data[0]['id']  # Return the first matching user
    return None  # No user found

def verify_password(user_id, password):
    """Check if the user's password is correct."""
    response = requests.post(
        f"{CLERK_BASE_URL}/users/{user_id}/verify_password",
        headers=HEADERS,
        json={"password": password}
    )

    if response.status_code == 200:
        return True
    else:
        return False
    
def create_session(user_id):
    """Create a session for the user."""
    response = requests.post(
        f"{CLERK_BASE_URL}/sessions",
        headers=HEADERS,
        json={"user_id": user_id}
    )
    return response.json()

@app.route("/signout", methods=["POST"])
def signout():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or "Bearer " not in auth_header:
            return jsonify({"error": "Session token missing"}), 400

        session_token = auth_header.split("Bearer ")[-1]  # Extract the session ID
        
        response = requests.post(
            f"{CLERK_BASE_URL}/sessions/{session_token}/revoke",
            headers=HEADERS
        )

        if response.status_code == 200:
            return jsonify({"message": "Sign out successful"}), 200
        else:
            return jsonify({"error": "Failed to sign out", "details": response.json()}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/check_session", methods=["GET", "POST"])
def check_session():
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization token is missing"}), 400
        
        session_token = auth_header.split("Bearer ")[-1]

        if not session_token:
            return jsonify({"error": "Invalid token format"}), 400

        return validate_session(session_token)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def validate_session(session_token):
    try:
        response = requests.get(
            f"{CLERK_BASE_URL}/sessions/{session_token}",
            headers=HEADERS
        )

        if response.status_code == 200:
            session_data = response.json()

            if session_data.get("status") == "revoked":
                return jsonify({"error": "Session has been revoked"}), 401
            else:
                return jsonify(session_data), 200

        return jsonify({"error": "Invalid session token"}), 401

    except Exception as e:
        return {"error": str(e)}, 500
    
def validate_user_id(user_id):
    """Compares session's user_id with user_id passed in. Used for validation"""
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization token is missing"}), 400
        
        session_token = auth_header.split("Bearer ")[-1]

        if not session_token:
            return jsonify({"error": "Invalid token format"}), 400

        response = requests.get(
            f"{CLERK_BASE_URL}/sessions/{session_token}",
            headers=HEADERS
        )

        res = response.json()
        if response.status_code == 200:
            # Session is valid, return session details
            return res["user_id"] == user_id
        
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500

@app.route("/retrieve_user_id", methods=['POST'])    
def retrieve_user_id():
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization token is missing"}), 400
        
        session_token = auth_header.split("Bearer ")[-1]

        if not session_token:
            return jsonify({"error": "Invalid token format"}), 400

        response = requests.get(
            f"{CLERK_BASE_URL}/sessions/{session_token}",
            headers=HEADERS
        )

        res = response.json()

        if response.status_code == 200:
            # Session is valid, return session details
            return jsonify({
                "user_id": res["user_id"]
                })
        else:
            # Session is invalid, return error
            return {"error": "Invalid session token"}, 401

    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Unauthorized", "message": "Session token is required"}), 401
        
        session_token = auth_header.split("Bearer ")[-1]
        response, status_code = validate_session(session_token)

        if status_code != 200:
            return response, status_code

        supabase_response = supabase.table("user").select("*").eq("user_id", user_id).execute()

        if supabase_response.data:
            return jsonify({"user": supabase_response.data[0]}), 200

        else:
            return jsonify({""
            "message": "user not found"
            }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_user/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        username = data.get("username")
        country = data.get("country")
        state = data.get("state")
        city = data.get("city")

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Unauthorized", "message": "Session token is required"}), 401
        
        session_token = auth_header.split("Bearer ")[-1]
        response, status_code = validate_session(session_token)

        if status_code != 200:
            return response, status_code
        
        valid = validate_user_id(user_id)
        if not valid:
            return jsonify({
                "message": "Not authorised to make changes."
            }), 401


        clerk_email_data = clerk_add_email(data, user_id)
        if clerk_email_data[0] == False:
            return clerk_email_data[1], clerk_email_data[2]
        else:

            # Step 3: Update User Password & Metadata in Clerk
            clerk_update_response = requests.patch(
                f"{CLERK_BASE_URL}/users/{user_id}",
                json={"password": password},
                headers=HEADERS
            )
            clerk_update_data = clerk_update_response.json()

            if clerk_update_response.status_code != 200:
                error_message = clerk_update_data.get('errors')[0].get('message', 'Unknown Error')
                return jsonify({"error": "Failed to update user details", "details": error_message}), clerk_update_response.status_code

            # Step 4: Update User Details in Supabase
            supabase_response = supabase.table("user").update({
                "username": username,
                "email": email,
                "country": country,
                "state": state,
                "city": city
            }).eq("user_id", user_id).execute()

            return jsonify({
                "message": "User updated successfully",
                "supabase": supabase_response.data
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def clerk_add_email(data, user_id):
    try:
        # Step 1: Add a new email to Clerk
        clerk_email_response = requests.post(
            f"{CLERK_BASE_URL}/email_addresses",
            json={
                "email_address": data['email'],
                "user_id": user_id,
                "verified": True,
                "primary": True
            },
            headers=HEADERS
        )

        # Handle response
        clerk_email_data = clerk_email_response.json()

        if clerk_email_response.status_code != 200:
            error_message = clerk_email_data.get('errors')[0].get('message', 'Unknown Error')
            return False, jsonify({"error": "Failed to add email", "details": error_message}), clerk_email_response.status_code

        clerk_email_new_idn = clerk_email_data.get('id')

        # Step 2: Fetch user details from Clerk
        clerk_user_response = requests.get(
            f"{CLERK_BASE_URL}/users/{user_id}",
            headers=HEADERS
        )

        clerk_user_data = clerk_user_response.json()
        clerk_emails = clerk_user_data.get("email_addresses", [])

        # Step 3: Remove old emails (except the new one)
        for email in clerk_emails:
            email_id = email.get('id')
            if email_id and email_id != clerk_email_new_idn:
                clerk_delete_response = requests.delete(
                    f"{CLERK_BASE_URL}/email_addresses/{email_id}",
                    headers=HEADERS
                )

                if clerk_delete_response.status_code != 200:
                    print(f"Failed to delete email {email_id}")
                    continue 

        return True, clerk_email_data, 200  # Return the newly added email details
    
    except Exception as e:
        return False, jsonify({"error": "Exception occurred", "details": str(e)}), 500

    
    
@app.route("/delete_user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Unauthorized", "message": "Session token is required"}), 401
        
        session_token = auth_header.split("Bearer ")[-1]
        response, status_code = validate_session(session_token)

        if status_code != 200:
            return response, status_code
        
        valid = validate_user_id(user_id)
        if not valid:
            return jsonify({
                "message": "Not authorised to delete."
            }), 401

        # Delete user from Clerk
        clerk_response = requests.delete(f"{CLERK_BASE_URL}/users/{user_id}", headers=HEADERS)
        if clerk_response.status_code != 200:
            return jsonify({"error": "Failed to delete user from Clerk"}), clerk_response.status_code

        # Remove user from Supabase
        supabase_response = supabase.table("user").delete().eq("user_id", user_id).execute()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
