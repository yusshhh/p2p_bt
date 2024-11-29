import os
import hashlib

FILE_STORAGE_DIR = "./files"
FILE_DEST = "./download"

def calculate_file_hash(file_path):
    hash_func = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def upload_file(file_path):
    if not os.path.exists(FILE_STORAGE_DIR):
        os.makedirs(FILE_STORAGE_DIR)
    file_name = os.path.basename(file_path)
    dest_path = os.path.join(FILE_STORAGE_DIR, file_name)
    os.replace(file_path, dest_path)
    print(f"File uploaded to {dest_path}")

def download_file(file_name):
    file_path = os.path.join(FILE_STORAGE_DIR, file_name)
    if os.path.exists(file_path):
        dest_path = os.path.join(FILE_DEST, file_name )
        os.replace(file_path,dest_path)
        print(f"File Downloaded to {dest_path}")
    else:
        print("File not found.")
