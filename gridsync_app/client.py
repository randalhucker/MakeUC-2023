import requests
import time

# Get the latest blockchain from the server
response = requests.get('http://localhost:5000/blockchain')

if response.status_code == 200:
    blockchain = response.json()
    last_block = blockchain[-1]
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
		'transaction_details': 'Buy 10 BTC',
		'supply': 2000,
		'price': 7000,
		'user': 'Randy'
	}
}

# Upload the data to the server
response = requests.post('http://localhost:5000/upload', json=data_to_upload)

if response.status_code == 201:
    print("Data added to the blockchain")
else:
    print("Failed to add data to the blockchain")