from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

STATUS_FILE = "status.txt"


def get_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status = f.read().strip()
            if status in ("on", "off"):
                return status
    return "unknown"


def save_status(status):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(status)


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/status", methods=["GET"])
def read_status():
    return jsonify({"status": get_status()})


@app.route("/status", methods=["POST"])
def write_status():
    data = request.get_json()

    status = data.get("status")

    if status not in ("on", "off"):
        return jsonify({"error": "Неверный статус"}), 400

    save_status(status)

    return jsonify({"success": True, "status": status})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

