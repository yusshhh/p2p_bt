import hashlib
import time

class Block:
    def __init__(self, index, timestamp, file_name, file_hash, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.file_name = file_name
        self.file_hash = file_hash
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{self.file_name}{self.file_hash}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "file_name": self.file_name,
            "file_hash": self.file_hash,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0", "0")

    def add_block(self, file_name, file_hash):
        previous_block = self.chain[-1]
        new_block = Block(
            len(self.chain), 
            time.time(), 
            file_name, 
            file_hash, 
            previous_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def to_dict(self):
        return [block.to_dict() for block in self.chain]
