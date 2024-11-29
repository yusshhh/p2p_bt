from flask import Flask, request, jsonify
import json
import time
import os
import hashlib

app = Flask(__name__)

BLOCKCHAIN_FILE = "blockchain.json"

# Load blockchain data
def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    return []

# Save blockchain data
def save_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(blockchain, f)

# Initialize blockchain
blockchain = load_blockchain()

# Calculate hash of a block
def calculate_block_hash(block):
    block_data = f"{block['index']}{block['timestamp']}{block['data']}{block['previous_hash']}"
    return hashlib.sha256(block_data.encode()).hexdigest()

# Add a new block
@app.route("/add_block", methods=["POST"])
def add_block():
    global blockchain
    data = request.json
    file_name = data.get("file_name")
    file_hash = data.get("file_hash")

    previous_hash = blockchain[-1]["hash"] if blockchain else "0"
    new_block = {
        "index": len(blockchain) + 1,
        "timestamp": time.time(),
        "data": {"file_name": file_name, "file_hash": file_hash},
        "previous_hash": previous_hash,
    }
    new_block["hash"] = calculate_block_hash(new_block)
    blockchain.append(new_block)
    save_blockchain(blockchain)
    return jsonify({"message": "Block added successfully!"}), 200

# Retrieve the blockchain
@app.route("/get_blockchain", methods=["GET"])
def get_blockchain():
    return jsonify({"blockchain": blockchain}), 200

# Validate the blockchain
def is_chain_valid(chain):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]

        if current_block["previous_hash"] != previous_block["hash"]:
            return False

        if calculate_block_hash(current_block) != current_block["hash"]:
            return False

    return True

@app.route("/validate_blockchain", methods=["GET"])
def validate_blockchain():
    valid = is_chain_valid(blockchain)
    return jsonify({"valid": valid}), 200

if __name__ == "__main__":
    app.run(debug=True)
