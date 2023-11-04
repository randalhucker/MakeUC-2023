import hashlib
from block import Block
from blockchain import Blockchain
from typing import List, Dict, Tuple
from flask import Response, request, jsonify

class GridSyncApp:
    def __init__(self):
        self.blockchain = Blockchain()
    
    # Check if a received block is valid
    def is_valid_block(self, dict_block: Dict[str, str], previous_block: Block) -> bool:
        if dict_block['index'] != previous_block.index + 1:
            return False
        if dict_block['previous_hash'] != previous_block.hash:
            return False
        # Add more validation rules as needed.

        return True

    # Check if a given Proof of Work is valid
    def is_valid_proof(self, last_proof: int, previous_hash: str, proof: int) -> bool:
        guess = f'{last_proof}{previous_hash}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Adjust the number of leading zeros as needed

    # Perform Proof of Work and find a valid nonce
    def proof_of_work(self, last_proof: int, previous_hash: str) -> int:
        proof = 0
        while not self.is_valid_proof(last_proof, previous_hash, proof):
            proof += 1
        return proof
 
    # Handle POST request to upload data
    def upload_data(self) -> Tuple[str, int]:
        data = request.get_json()
        last_block = self.blockchain.get_last_block()
        proof = self.proof_of_work(last_block.proof, last_block.hash)
        v_block = self.is_valid_block(data, last_block)
        v_proof = self.is_valid_proof(last_block.proof, last_block.hash, proof)
        if v_block and v_proof:
            self.blockchain.add_block(data, proof)
            return ("Data added to the blockchain", 201)
        else:
            return ("Invalid data or proof of work", 400)

    # Handle GET request to retrieve the entire blockchain
    def get_blockchain(self) -> Response:
        chain: List[Block] = []
        previous_hash = "0"
        for block in self.blockchain.chain:
            chain.append(block.to_dict())
            previous_hash = block.hash
        return jsonify(chain)

    # Handle GET request to retrieve the last block in the blockchain
    def get_last_block(self) -> Response:
        last_block = self.blockchain.get_last_block()
        return jsonify(last_block.to_dict())

    # Get the length of the blockchain
    def get_blockchain_length(self) -> int:
        return len(self.blockchain.chain)
