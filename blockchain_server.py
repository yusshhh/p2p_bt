from flask import Flask, request, jsonify, send_from_directory
from hashlib import sha256
import os
import time

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

blockchain = []

def calculate_hash(index, previous_hash, timestamp, data):
    block_string = f"{index}{previous_hash}{timestamp}{data}"
    return sha256(block_string.encode()).hexdigest()

@app.route("/add_block", methods=["POST"])
def add_block():
    data = request.json
    file_name = data["file_name"]
    file_hash = data["file_hash"]
    if not os.path.exists(os.path.join(UPLOAD_FOLDER, file_name)):
        return jsonify({"message": "File does not exist on server"}), 404

    previous_block = blockchain[-1] if blockchain else {"hash": "0"}
    new_block = {
        "index": len(blockchain),
        "timestamp": time.time(),
        "data": {"file_name": file_name, "file_hash": file_hash},
        "previous_hash": previous_block["hash"],
        "hash": calculate_hash(len(blockchain), previous_block["hash"], time.time(), {"file_name": file_name, "file_hash": file_hash}),
    }
    blockchain.append(new_block)
    return jsonify({"message": "Block added successfully", "block": new_block})

@app.route("/download_file/<file_name>", methods=["GET"])
def download_file(file_name):
    if os.path.exists(os.path.join(UPLOAD_FOLDER, file_name)):
        return send_from_directory(UPLOAD_FOLDER, file_name, as_attachment=True)
    return jsonify({"message": "File not found"}), 404

if __name__ == "__main__":
    blockchain.append({
        "index": 0,
        "timestamp": time.time(),
        "data": "Genesis Block",
        "previous_hash": "0",
        "hash": calculate_hash(0, "0", time.time(), "Genesis Block"),
    })
    app.run(port=8080)
