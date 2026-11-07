from flask import Flask, render_template, request
import requests
import base64

# Replace this with your real API endpoint!
API_URL = "https://your-api.com/detect"

app = Flask(__name__)

def detect_tumor(file):
    image_bytes = file.read()
    image_b64 = base64.b64encode(image_bytes).decode()
    data = {"image": image_b64}
    headers = {"Content-Type": "application/json"}

    resp = requests.post(API_URL, json=data, headers=headers)
    if resp.status_code != 200:
        return (False, "API error: " + resp.text)
    prediction = resp.json().get("prediction")
    if prediction == "yes":
        return (True, "Tumor Detected")
    elif prediction == "no":
        return (True, "No Tumor Detected")
    else:
        return (False, "Unexpected API response.")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            success, res = detect_tumor(file)
            if success:
                result = res
            else:
                error = res
        else:
            error = "No file uploaded."
    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
    