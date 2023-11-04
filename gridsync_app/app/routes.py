from app import app
from gridsync.runtime import GridSyncApp

gridsync = GridSyncApp()

@app.route('/upload', methods=['POST'])
def upload_block():
    return gridsync.upload_data()


@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return gridsync.get_blockchain()

@app.route('/blockchain/last', methods=['GET'])
def get_last_block():
    return gridsync.get_last_block()

@app.route('/blockchain/length', methods=['GET'])
def get_blockchain_length():
    return gridsync.get_blockchain_length()