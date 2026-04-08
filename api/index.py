from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import os

app = Flask(__name__)
# Emojis properly display করার জন্য
app.config['JSON_AS_ASCII'] = False

# আপনার কাস্টম কপিরাইট ও ডেভেলপার নাম
COPYRIGHT_STRING = "@nexxonhackers | Developed by CREATOR SHYAMCHAND"

# আউটপুটে কি কি তথ্য কোন সিরিয়ালে থাকবে
DESIRED_ORDER = [
    "Owner Name", "Father's Name", "Owner Serial No", "Model Name", "Maker Model",
    "Vehicle Class", "Fuel Type", "Fuel Norms", "Registration Date", "Insurance Company",
    "Insurance No", "Insurance Expiry", "Insurance Upto", "Fitness Upto", "Tax Upto",
    "PUC No", "PUC Upto", "Financier Name", "Registered RTO", "Address", "City Name", "Phone"
]

def get_vehicle_details(rc_number: str) -> dict:
    rc = rc_number.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "Referer": "https://vahanx.in/rc-search",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}

    def get_value(label):
        try:
            # vahanx.in এর HTML স্ট্রাকচার অনুযায়ী ডাটা খোঁজা
            span = soup.find("span", string=label)
            if span:
                div = span.find_parent("div")
                return div.find("p").get_text(strip=True)
            return "N/A"
        except:
            return "N/A"

    data = {key: get_value(key) for key in DESIRED_ORDER}
    return data

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🚗 Vehicle Info API is running!",
        "developer": "CREATOR SHYAMCHAND",
        "usage": "/lookup?rc=WB02XXXXXX"
    })

@app.route("/lookup", methods=["GET"])
def lookup_vehicle():
    rc_number = request.args.get("rc")
    if not rc_number:
        return jsonify({
            "error": "Please provide ?rc= parameter",
            "copyright": COPYRIGHT_STRING
        }), 400

    details = get_vehicle_details(rc_number)
    
    # সিরিয়াল অনুযায়ী সাজানো
    ordered_details = OrderedDict()
    for key in DESIRED_ORDER:
        if key in details:
            ordered_details[key] = details[key]
    
    ordered_details["copyright"] = COPYRIGHT_STRING
    ordered_details["disclaimer"] = "For Educational Purposes Only"
    
    return jsonify(ordered_details)

# Vercel app object
app_handler = app
            
