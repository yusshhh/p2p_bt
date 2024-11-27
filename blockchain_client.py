import requests

BASE_URL = "http://localhost:8080"

def add_block(file_name, file_hash):
    response = requests.post(
        f"{BASE_URL}/add_block",
        json={"file_name": file_name, "file_hash": file_hash},
    )
    if response.status_code == 201:
        print("Block added to the blockchain!")
    else:
        print(f"Failed to add block: {response.text}")

def get_blockchain():
    response = requests.get(f"{BASE_URL}/blockchain")
    if response.status_code == 200:
        blockchain = response.json()
        print("Blockchain:")
        for block in blockchain:
            print(block)
    else:
        print(f"Failed to fetch blockchain: {response.text}")

def validate_blockchain():
    response = requests.get(f"{BASE_URL}/validate")
    print(response.text)
