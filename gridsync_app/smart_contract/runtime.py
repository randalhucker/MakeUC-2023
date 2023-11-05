from typing import Dict
import hashlib
import time
import random

"""
example_contract = {
    self.owner: "0x1234567890",
    self.buyer: "0x0987654321",
    self.address: "0x1234567890abcdef",
    self.executed: True,
    self.data: {
		"amount": 1000W,
		"price": 1000/kw,
	}
 """

class SmartContract:
	def __init__(self, owner: str, data: Dict[str, str]):
		self.owner: str = owner
		self.buyer: str = ""
		self.data: Dict[str, str] = data # The data that the contract will operate on
		self.address: str = self.generate_unique_contract_id(owner)
		self.executed: bool = False

	def execute(self, data: Dict[str, str]) -> Dict[str, str]:
		# Execute the contract and return the result
		self.executed = True
		self.buyer = data['s_address']
		# TODO Add logic for executing the contract
		return self.data

	def generate_unique_contract_id(self, owner_id):
		# Generate a contract ID based on the current timestamp, owner ID, and some random value
		unique_string = f"{time.time()}{owner_id}{random.randint(1, 1000000)}"
		contract_id = hashlib.sha256(unique_string.encode()).hexdigest()
		return contract_id
		
	def to_dict(self) -> Dict[str, str]:
		return {
			'owner': self.owner,
			'data': self.data,
			'address': self.address,
			'executed': self.executed
		}