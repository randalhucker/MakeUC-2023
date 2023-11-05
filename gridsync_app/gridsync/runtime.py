import hashlib
from block import Block
from blockchain import Blockchain
from typing import List, Dict, Tuple
from flask import Response, request, jsonify
from database.runtime import DataBase
from models.runtime import PredictedLoadModel
from smart_contract import SmartContract
from typing import List, Dict
import pickle

class GridSyncApp:
    def __init__(self):
        self.blockchain = Blockchain()
        self.database = DataBase()
        self.models: Dict[str, PredictedLoadModel]= {}
        try:
            # Connect to the database
            print("Connecting to database")
            self.database.connect()
            print("Connected to database")
            
            self.database.delete_collection("Wooster")
            self.database.models.delete_collection()
            
            self.database.create_collection("Wooster", "Wooster_Data")
                
            model = PredictedLoadModel(self.database, "Wooster")
            self.models["Wooster"] = model
            model.train(self.database)
            
        except Exception as e:
            print(e)
    
    # Check if a received block is valid
    def is_valid_block(self, dict_block: Dict[str, str], previous_block: Block) -> bool:
        if dict_block['index'] != previous_block.index + 1:
            return False
        if dict_block['previous_hash'] != previous_block.previous_hash:
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
    def upload_data(self, data) -> Tuple[int, int]:
        last_block = self.blockchain.get_last_block()
        proof = self.proof_of_work(last_block.proof, last_block.hash)
        v_block = self.is_valid_block(data, last_block)
        v_proof = self.is_valid_proof(last_block.proof, last_block.hash, proof)
        if v_block and v_proof:
            self.blockchain.add_block(data, proof)
            return (data['index'], 201)
        else:
            return (0, 400)

    # Handle GET request to retrieve the entire blockchain
    def get_blockchain(self) -> Response:
        chain: List[Block] = []
        previous_hash = "0"
        for block in self.blockchain.chain:
            chain.append(block.to_dict(previous_hash))
            previous_hash = block.hash
        return jsonify(chain)

    # Handle GET request to retrieve the last block in the blockchain
    def get_last_block(self) -> Response:
        last_block = self.blockchain.get_last_block()
        return jsonify(last_block.to_dict(last_block.previous_hash))

    # Get the length of the blockchain
    def get_blockchain_length(self) -> Response:
        return jsonify(len(self.blockchain.chain))

    # TODO Fix route for deploying smart contracts
    def deploy_contract(self, data) -> Tuple[str, int]:
        owner = data['s_address']
        data = data['data']
        contract = SmartContract(owner, data)

        # Store the contract in the current block
        self.blockchain.contracts.append(contract)
        return (contract.address, 201)
    
    def execute_contract(self, contract_id: str, data) -> Tuple[str, int]:
        contract = self.blockchain.find_contract_by_id(contract_id)
        if contract:
            data_to_upload = contract.execute(self.blockchain, data)
            self.upload_data(data_to_upload)
            return "Contract executed successfully", 200
        else:
            return "Contract not found", 404
    
    def get_contract_data(self, contract_id: str) -> Response:
        contract = self.blockchain.find_contract_by_id(contract_id)
        if contract:
            return jsonify(contract.to_dict())
        else:
            return "Contract not found", 404
        
    def get_all_contracts(self) -> Response:
        contracts = [contract.to_dict() for contract in self.blockchain.find_all_contracts()]
        return jsonify(contracts)
    
    def make_prediction(self, data) -> Response:
        """This method is used to make a prediction for the estimated load requirement for a given node in the grid for a given week
        Example request:
        data = {
            "collection_name": "Wooster",
            "year": 2021,
            "month": 1,
            "day": 1,
            "temperature": 0
        }

        Args:
            data (Dict): A dictionary containing the collection name, year, month, day, hour, and temperature

        Returns:
            Response: A response containing the predicted load requirement for each hour (averaged for the given week)
        """
        collection_name = data['collection_name']
        model: PredictedLoadModel = self.models[collection_name]
        year = data['year']
        month = data['month']
        day = data['day']
        temperature = data['temperature']
        prediction = model.predict_weekly_loads(year, month, day, temperature)
        return jsonify(prediction)
        