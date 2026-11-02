import os
import json
import logging
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder=".")

# чтение конфигурационного файла
CONFIG_FILE = "/work/config.json"
config = {"max_factorial_limit": 20}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config.update(json.load(f))

# логирования в файл 
LOG_FILE = "/work/logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# чтение конфигурации из переменных окружения
APP_ENV = os.getenv("APP_ENV", "development")
APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello, World!")
PORT = int(os.getenv("PORT", 8000))

@app.before_request
def log_requests():
    # логируем каждый входящий HTTP запрос
    msg = f"Method: {request.method}, Path: {request.path}, IP: {request.remote_addr}, Env: {APP_ENV}"
    logging.info(msg)

@app.route("/")
def index():
    return render_template("index.html", message=APP_MESSAGE, env=APP_ENV)

@app.route("/calculate")
def calculate():
    # Произвольная логика - вычисление факториала числа ?n=x
    try:
        n = int(request.args.get("n", 5))
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