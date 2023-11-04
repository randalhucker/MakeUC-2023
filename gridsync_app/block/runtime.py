import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index: int = index
        self.previous_hash: str = previous_hash
        self.timestamp: int = timestamp
        self.data = data
        self.proof: int = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        return hashlib.sha256(str(self.index).encode() +
                              str(self.previous_hash).encode() +
                              str(self.timestamp).encode() +
                              str(self.data).encode() +
                              str(self.proof).encode()).hexdigest()
        
    def to_dict(self) -> dict:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }
