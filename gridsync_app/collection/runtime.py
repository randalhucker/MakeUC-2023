import pymongo
import pandas as pd
import numpy as np
import csv
from pymongo.database import Database
from typing import Dict


# DataBase class used to interat with MongoDB for storing and retrieving records and models
class Collection:
    def __init__(self, db: Database, name: str, csv_name: str = None):
        self.name = name
        self.collection = db[name]
        if csv_name is not None:
            self.create_collection(csv_name)

    def create_collection(self, csv_name: str) -> None:
        # Open and read the CSV file
        with open(
            f"/Users/randyhucker/Documents/GitHub/MakeUC-2023/gridsync_app/collection/{csv_name}.csv",
            "r",
        ) as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                # Insert each row as a document in the collection
                # {'_id': ObjectId('6546fbfc09221c2c42714308'), 'year': 2022, 'month': 11, 'day': 20, 'hour': '500', 'temperature': -8, 'load_requirement': 10135608}
                self.collection.insert_one(self.convert_dict(row))

    def delete_collection(self) -> None:
        self.collection.drop()

    def convert_dict(self, input_dict):
        # Extract the date and time components from the input
        try:
            lst_date = input_dict["LST_DATE"]
            lst_time = input_dict["LST_TIME"]

            year = int(lst_date[0:4])
            month = int(lst_date[4:6])
            day = int(lst_date[6:8])

        except ValueError:
            # Handle invalid date or time values here, e.g., set defaults or raise an exception
            return {}

        # Convert temperature and load to float
        temperature = float(input_dict["T_HR_AVG"])
        load_requirement = float(input_dict["TOT_LOAD"])

        # Create the new dictionary
        new_dict = {
            "year": year,
            "month": month,
            "day": day,
            "hour": lst_time,  # Multiplying by 100 to match the desired format
            "temperature": round(temperature),  # Rounding to the nearest integer
            "load_requirement": round(
                load_requirement
            ),  # Rounding to the nearest integer
        }

        return new_dict

    # Get Records from MongoDB
    # Takes in ID number and returns all records with that ID number
    def get_records(self) -> pd.DataFrame:
        # Query the collection to retrieve all documents
        cursor = self.collection.find()
        documents = list(cursor)

        return pd.DataFrame(documents)

    # Upload Records to MongoDB
    # Takes in a record and uploads it to MongoDB
    def upload_record(self, record) -> None:
        # Upload records to MongoDB
        self.collection.insert_one(record)

    # Get Models from MongoDB
    # Takes in ID number and returns the pickle dump version of the model with that ID number
    def get_model(self, model_name):
        # Get model from collection
        model = self.collection.find_one({"_id": model_name})
        return model

    # Upload Model to MongoDB
    # Takes in the pickle dump version of a model and uploads it to MongoDB
    def upload_model(self, model_name: str, model, scaler) -> None:
        if self.collection.find_one({"_id": model_name}) == None:
            # Upload model to MongoDB
            self.collection.insert_one({"_id": model_name, "model": model, "scaler": scaler})
        else:
            # Update model in MongoDB
            self.collection.update_one({"_id": model_name}, {"$set": {"model": model, "scaler": scaler}})
