import requests
import time

# Get the latest blockchain from the server
response = requests.get('http://127.0.0.1:5000/blockchain/last')

if response.status_code == 200:
    last_block = response.json()
    previous_hash = last_block['previous_hash']  # Get the latest block's hash
    index = last_block['index'] + 1
else:
    print("Failed to retrieve the blockchain")
    index = 0
    previous_hash = "0"  # Use the Genesis block's hash when the blockchain is empty

# Prepare data with the correct index and previous hash
data_to_upload = {
    'index': index,
    'previous_hash': previous_hash,
    'timestamp': int(time.time()),
    'data': {
		's_address': 'Alice',
        'r_address': 'Bob',
        'amount': '12KW',
        'price': '0.12$/KW',
        'signature': 'Alice\'s Signature',
	}
}

# Upload the data to the server
response = requests.post('http://127.0.0.1:5000/blockchain/transaction', json=data_to_upload)

if response.status_code == 201:
    print("Data added to the blockchain")
else:
    print("Failed to add data to the blockchain")