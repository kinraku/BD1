import os
import json
import logging
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder=".")

CONFIG_FILE = "/work/config.json"
LOG_FILE = "/work/logs/app.log"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

APP_ENV = os.getenv("APP_ENV", "development")
PORT = int(os.getenv("PORT", 8000))

def get_config():
    config = {"app_message": "Hello, World!", "max_factorial_limit": 20}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config.update(json.load(f))
        except Exception:
            pass
    return config

@app.before_request
def log_requests():
    msg = f"Method: {request.method}, Path: {request.path}, IP: {request.remote_addr}, Env: {APP_ENV}"
    logging.info(msg)

@app.route("/")
def index():
    config = get_config()
    limit = config.get("max_factorial_limit", 20)
    return render_template(
        "index.html", 
        message=config.get("app_message", "Hello, World!"), 
        env=APP_ENV,
        limit=limit
    )

@app.route("/calculate")
def calculate():
    try:
        n = int(request.args.get("n", 5))
        config = get_config()
        max_limit = config.get("max_factorial_limit", 20)
        if n < 0 or n > max_limit:
            return jsonify({"error": "число должно быть в диапазоне от 0 до 20"}), 400
        
        import math
        result = math.factorial(n)
        return jsonify({"number": n, "factorial": result, "status": "success"})
    except ValueError:
        return jsonify({"error": "параметр 'n' должен быть целым числом"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)