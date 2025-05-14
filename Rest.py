from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify({"message": "pong"})

if __name__ == "__main__":
    app.run(port=5000)
