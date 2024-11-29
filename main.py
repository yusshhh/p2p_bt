from blockchain_client import add_block, get_blockchain, verify_blockchain
from file_manager import calculate_file_hash, upload_file, download_file

def main():
    while True:
        print("\n=== File Sharing Blockchain ===")
        print("1. Upload File")
        print("2. Download File")
        print("3. Display Blockchain")
        print("4. Verify Blockchain Integrity")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            file_path = input("Enter the path of the file to upload: ")
            file_hash = calculate_file_hash(file_path)
            upload_file(file_path)
            add_block(file_path, file_hash)

        elif choice == "2":
            file_name = input("Enter the name of the file to download: ")
            download_file(file_name)

        elif choice == "3":
            blockchain = get_blockchain()
            for block in blockchain:
                print(block)

        elif choice == "4":
            verify_blockchain()

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
