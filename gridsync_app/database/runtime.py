import pymongo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# DataBase class used to interat with MongoDB for storing and retrieving records and models
class DataBase:
    def __init__(self):
        # MongoDB connection settings
        self.mongo_host = "localhost"  # Change this to MongoDB server hostname or IP address
        self.mongo_port = 27017  # Change this to MongoDB serve port
        self.database_name = "database"  # Change this to your database name
        self.collection_name = "collection"  # Change this to your collection name

    # Get Records from MongoDB
    # Takes in ID number and returns all records with that ID number
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
    
    def get_most_recent_record(self, ID):
        # Connect to MongoDB
        client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        db = client[self.database_name]
        collection = db[self.collection_name]

        # Get most recent record from MongoDB with specified ID number
        #records = collection.find({"ID": ID})

        # Convert record to pandas dataframe
        records_df = pd.DataFrame(list(records))

        # Close MongoDB connection
        client.close()

        return records_df.iloc[-1]
    
    # Upload Records to MongoDB
    # Takes in a record and uploads it to MongoDB
    def upload_record(self, record):
        # Connect to MongoDB
        client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        db = client[self.database_name]
        collection = db[self.collection_name]

        # Upload records to MongoDB
        collection.insert_one(record)

        # Close MongoDB connection
        client.close()
    
    # Get Models from MongoDB
    # Takes in ID number and returns the pickle dump version of the model with that ID number
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
    
    # Upload Model to MongoDB
    # Takes in the pickle dump version of a model and uploads it to MongoDB
    def upload_model(self, Model_ID, model):
        # Connect to MongoDB
        client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        db = client[self.database_name]
        collection = db[self.collection_name]

        if (collection.find_one({"Model ID": Model_ID}) == None):
            # Upload model to MongoDB
            collection.insert_one(model)
        else:
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
