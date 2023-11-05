from block import Block
from smart_contract import SmartContract
import time
from typing import List, Dict

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.contracts: List[SmartContract] = []  # List of contracts in this blockchain\
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        # Create the first block in the chain
        genesis_block = Block(0, "0", int(time.time()), {"Genesis Block": "First Block"}, 0)
        self.chain.append(genesis_block)

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: Dict[str,str], proof: int) -> None:
        previous_block = self.get_last_block()
        new_block = Block(previous_block.index + 1, previous_block.hash, int(time.time()), data['data'], proof)
        self.chain.append(new_block)
        
    def find_contract_by_id(self, contract_id: str) -> SmartContract:
        # Retrieve the contract data from the blockchain and return it in JSON format
        for contract in self.contracts:
            if contract.address == contract_id:
                return contract
            
    def find_all_contracts(self) -> List[SmartContract]:
        return self.contracts
