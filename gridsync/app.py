from flask import Flask, request, jsonify
from blockchain import Blockchain
from block import Block
import hashlib
from typing import List, Dict

app = Flask(__name__)
blockchain = Blockchain()

def is_valid_block(dict_block: Dict[str, str], previous_block: Block):
    if dict_block['index'] != previous_block.index + 1:
        return False

    print("Hash Compare")
    print(dict_block['previous_hash'])
    print(previous_block.hash)
    if dict_block['previous_hash'] != previous_block.previous_hash:
        return False
    # Add more validation rules as needed.
    return True

def proof_of_work(last_proof: int, previous_hash: str) -> int:
    proof = 0
    while not is_valid_proof(last_proof, previous_hash, proof):
        proof += 1
    return proof

def is_valid_proof(last_proof: int, previous_hash: str, proof: int) -> bool:
    guess = f'{last_proof}{previous_hash}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"  # Adjust the number of leading zeros as needed

@app.route('/upload', methods=['POST'])
def upload_data() -> str:
    data = request.get_json()
    # print(data)
    last_block = blockchain.get_last_block()
    print("last_block hash")
    print(last_block.previous_hash)
    proof = proof_of_work(last_block.proof, last_block.hash)
    print("proof")
    print(proof)
    
    v_block = is_valid_block(data, last_block)
    print(v_block)
    v_proof = is_valid_proof(last_block.proof, last_block.hash, proof)
    print(v_proof)
    
    if v_block and v_proof:
        blockchain.add_block(data, proof)
        return "Data added to the blockchain", 201
    else:
        return "Invalid data or proof of work", 400

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain: List[Block] = []
    previous_hash = "0"  # Initialize with the hash of the Genesis block
    for block in blockchain.chain:
        chain.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'proof': block.proof,
            'previous_hash': previous_hash  # Include the previous block's hash
        })
        previous_hash = block.hash  # Update previous_hash for the next block
    return jsonify(chain)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)