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
# Load from Railway environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO", "stablesterling/Njora1")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]

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

    if response.status_code in [200, 201]:
        return jsonify({
            "status": "success",
            "filename": filename,
            "github_url": response.json().get("content", {}).get("html_url", "")
        }), 200
    else:
        return jsonify({
            "status": "error",
            "details": response.json()
        }), response.status_code


# ===============================
# RUN APP (Railway compatible)
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
