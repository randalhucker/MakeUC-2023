import pymongo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

class DataBase:
    def __init__(self):
        # MongoDB connection settings
        self.mongo_host = "localhost"  # Change this to MongoDB server hostname or IP address
        self.mongo_port = 27017  # Change this to MongoDB serve port
        self.database_name = "database"  # Change this to your database name
        self.collection_name = "collection"  # Change this to your collection name

    def get_records(self, ID):
        # Connect to MongoDB
        client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        db = client[self.database_name]
        collection = db[self.collection_name]

        # Get all records from MongoDB with specified ID number
        records = collection.find({"ID": ID})

        # Convert records to pandas dataframe
        records_df = pd.DataFrame(list(records))

        # Close MongoDB connection
        client.close()

        return records_df
    
    def upload_records(self, records_df):
        # Connect to MongoDB
        client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        db = client[self.database_name]
        collection = db[self.collection_name]
        
        # Convert records to dictionary
        records_dict = records_df.to_dict()

        # Upload records to MongoDB
        collection.insert_many(records_dict)

        # Close MongoDB connection
        client.close()
    
    def get_model(self, Model_ID):
        # Connect to MongoDB
        client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        db = client[self.database_name]
        collection = db[self.collection_name]

        # Get all records from MongoDB with specified ID number
        model = collection.find_one({"Model ID": Model_ID})

        # Close MongoDB connection
        client.close()

        return model
    
    def update_model(self, Model_ID, model):
        # Connect to MongoDB
        client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        db = client[self.database_name]
        collection = db[self.collection_name]

        # Update model in MongoDB
        collection.update_one({"Model ID": Model_ID}, {"$set": model})

        # Close MongoDB connection
        client.close()

    # features (each node will have its own model that is stored in the database)
    # ID: _identification_ (used only for classifying records and models)
    # time data (calculate from seconds since epoch)
        # year: _year_
        # month: _month_
        # season: _season_
        # day: _day_
        # hour: _hour_
    # weather data
        # temperature: _temperature_
    # output
        # load_requirement: _load_requirement_
