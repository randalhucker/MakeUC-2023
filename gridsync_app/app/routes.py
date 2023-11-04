from app import app
from flask import request
from gridsync.runtime import GridSyncApp

gridsync = GridSyncApp()

@app.route('/blockchain/upload', methods=['POST'])
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