import requests

BASE_URL = "http://127.0.0.1:5000"

def add_block(file_name, file_hash):
    response = requests.post(
        f"{BASE_URL}/add_block",
        json={"file_name": file_name, "file_hash": file_hash},
    )
    if response.status_code == 200:
        print("Block added to the blockchain!")
    else:
        print("Error adding block:", response.text)

def get_blockchain():
    response = requests.get(f"{BASE_URL}/get_blockchain")
    if response.status_code == 200:
        return response.json().get("blockchain", [])
    else:
        print("Error fetching blockchain:", response.text)
        return []

def verify_blockchain():
    response = requests.get(f"{BASE_URL}/validate_blockchain")
    if response.status_code == 200:
        is_valid = response.json().get("valid", False)
        print("Blockchain integrity:", "Valid" if is_valid else "Corrupted")
    else:
        print("Error verifying blockchain integrity.")
