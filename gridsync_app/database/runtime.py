from collection import Collection
import pymongo
from pymongo.database import Database
import pandas as pd
from typing import List

class DataBase:
	def __init__(self):
		# MongoDB connection settings
		self.mongo_host = "localhost"
		self.mongo_port = 27017
		self.database_name = "gridsync"
		self.collections: List[Collection] = []
		self.client: pymongo.MongoClient = None
		self.db: Database = None
		self.models: Collection = None
  
	def connect(self) -> None:
		self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
		self.db = self.client[self.database_name]
		self.models = Collection(self.db, "models")
  
	def create_collection(self, collection_name: str, csv_name: str) -> None:
		collection = Collection(self.db, collection_name, csv_name)
		self.collections.append(collection)
  
	def delete_collection(self, collection_name: str) -> None:
		collection = self.get_collection(collection_name)
		if collection is not None:
			collection.delete_collection()
			self.collections.remove(collection)
  
	def get_collection(self, collection_name: str) -> Collection:
		for collection in self.collections:
			if collection.name == collection_name:
				return collection
		return None

	def get_records(self, collection_name: str) -> pd.DataFrame:
		collection = self.get_collection(collection_name)
		return collection.get_records()

	def close(self) -> None:
		self.client.close()