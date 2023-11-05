from app import app
from flask import request, Response
from typing import Tuple
from gridsync.runtime import GridSyncApp

gridsync = GridSyncApp()

@app.route('/blockchain/transaction', methods=['POST'])
def upload_block():
    data = request.get_json()
    return gridsync.upload_data(data)

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return gridsync.get_blockchain()

@app.route('/blockchain/last', methods=['GET'])
def get_last_block():
    return gridsync.get_last_block()

@app.route('/blockchain/length', methods=['GET'])
def get_blockchain_length():
    return gridsync.get_blockchain_length()

# Add a new route for deploying smart contracts
@app.route('/deploy_contract', methods=['POST'])
def deploy_contract() -> Tuple[str, int]:
    data = request.get_json()
    return gridsync.deploy_contract(data)

# Add a new route for executing a smart contract
@app.route('/execute_contract/<contract_id>', methods=['POST'])
def execute_contract(contract_id: str) -> Tuple[str, int]:
    data = request.get_json()
    return gridsync.execute_contract(contract_id, data)

# Add a new route for querying contract data
@app.route('/contract_data/<contract_id>', methods=['GET'])
def get_contract_data(contract_id: str) -> Response:
    return gridsync.get_contract_data(contract_id)

# Add a new route for querying all contracts
@app.route('/all_contracts', methods=['GET'])
def get_all_contracts() -> Response:
    return gridsync.get_all_contracts()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    return gridsync.make_prediction(data)