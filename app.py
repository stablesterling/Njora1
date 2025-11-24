import base64
import os
from flask import Flask, request, jsonify
import requests
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_TOKEN = "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"
REPO = "stablesterling/Njora1"

@app.post("/upload")
def upload_image():
    file = request.files["file"]
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    filename = datetime.now().strftime("%Y%m%d%H%M%S_") + file.filename
    upload_path = f"uploads/{filename}"

    file_content = base64.b64encode(file.read()).decode("utf-8")

    url = f"https://api.github.com/repos/{REPO}/contents/{upload_path}"
    
    payload = {
        "message": f"Uploaded {filename}",
        "content": file_content
    }

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.put(url, json=payload, headers=headers)
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(port=5000, debug=True)
