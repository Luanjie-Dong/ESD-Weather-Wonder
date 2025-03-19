from flask import Flask, request, jsonify
from flask_cors import CORS  
from encoder import encode_location_by_name , decode_location


app = Flask(__name__)
CORS(app)

@app.route("/encode",methods=['POST'])
def encode_location_func():

    """
    Input: Address/Location --> E.g Singapore / 57 Margaret St Cottesloe
    Output: Country , Town , Latitude , Longitude , formatted location 
    """

    data = request.get_json()
    if not data:
            return jsonify({"error": "No JSON data provided"}), 400
    
    location_data = data.get("location","")
    encoded_data = encode_location_by_name(location_data)

    if encoded_data != "":
        return encoded_data
    else:
        return f"Error encoding {location_data}", 404


@app.route("/decode",methods=['POST'])
def decode_location_func():

    """
    Input: Latitude , Longitude 
    Output: Address/Location --> E.g Singapore / 57 Margaret St Cottesloe
    """

    data = request.get_json()
    if not data:
            return jsonify({"error": "No JSON data provided"}), 400
    
    location_lat = data.get("lat","")
    location_lon = data.get("lon","")

    decoded_data = decode_location(location_lat,location_lon)

    if decoded_data != "":
        return decoded_data
    else:
        return f"ERROR decoding with {location_lat} , {location_lon}", 404



if __name__=="__main__":
     app.run('0.0.0.0',port=5004,debug=True)