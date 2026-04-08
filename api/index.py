from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# আপনার JWT টোকেন
JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI1ODM4NTgzMzg4IiwianRpIjoiNjkzMGRhMjctOTBjNi00OTcyLTlkYjYtMjdhOTI2NzQxYjU5IiwiZXhwIjoxNzg1NDE1OTk0fQ.rZJMVGi-o-PmTH-GkpvOBowqrY_FflHVxRuW1-Ro27y2uNTiSwLXR0ohDoFXPcBdmwyyy70fjfUHU89By7_eVtpKZMH5hganj0PngE8r_ZxzvrmJApYlpKKjDP4SWPtNDLSFi30e9FOXUva1hihJxoGUUibTDAwX_vEM8fZQ_8E"

@app.route("/")
def home():
    return jsonify({
        "status": "TG Info API is Live",
        "developer": "CREATOR SHYAMCHAND",
        "usage": "/user-details?user=USER_ID"
    })

@app.route("/user-details")
def user_details():
    user_id = request.args.get("user")

    if not user_id:
        return jsonify({"success": False, "error": "Missing user ID parameter (?user=12345678)"}), 400

    url = f"https://funstat.info/api/v1/users/{user_id}/stats_min"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {JWT}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        # যদি টোকেন এক্সপায়ার হয় বা অন্য কোনো এরর আসে
        if response.status_code == 401:
            return jsonify({"success": False, "error": "Unauthorized: JWT Token may be expired"}), 401
            
        if response.status_code != 200:
            return jsonify({
                "success": False, 
                "error": "Failed to fetch user info", 
                "status_code": response.status_code
            }), 500
        
        data = response.json()
        
        # আপনার কাস্টম ক্রেডিট যুক্ত করা
        return jsonify({
            "success": True, 
            "data": data,
            "credits": "Developed by CREATOR SHYAMCHAND"
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Vercel handler
app_handler = app
