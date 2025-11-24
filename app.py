import base64
from datetime import datetime
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ===============================
# CONFIGURATION (HARDCODED TOKEN)
# ===============================
GITHUB_TOKEN = "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"  # <-- Replace with your GitHub personal access token
REPO = "stablesterling/Njora"         # <-- Your GitHub repo in username/repo format

@app.post("/upload")
def upload_image():
    file = request.files.get("file")
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    # Generate a unique filename
    filename = datetime.now().strftime("%Y%m%d%H%M%S_") + file.filename
    upload_path = f"uploads/{filename}"

    # Convert file to base64
    file_content = base64.b64encode(file.read()).decode("utf-8")

    # GitHub API URL
    url = f"https://api.github.com/repos/{REPO}/contents/{upload_path}"
    
    # Request payload
    payload = {
        "message": f"Uploaded {filename}",
        "content": file_content
    }

    # Request headers
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    # Send PUT request to GitHub
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code in [200, 201]:
        return jsonify({"success": True, "data": response.json()})
    else:
        return jsonify({"success": False, "error": response.json()}), response.status_code

if __name__ == "__main__":
    app.run(port=5000, debug=True)
