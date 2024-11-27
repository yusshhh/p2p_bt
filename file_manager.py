import hashlib
import os

def calculate_file_hash(file_path):
    """Calculates the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def upload_file(file_path):
    """Mock upload of a file."""
    if os.path.exists(file_path):
        print(f"File '{file_path}' uploaded successfully!")
    else:
        print(f"File '{file_path}' does not exist.")

def download_file(file_name, output_path):
    """Mock download of a file."""
    print(f"Mock: Downloading file '{file_name}' to '{output_path}'...")
