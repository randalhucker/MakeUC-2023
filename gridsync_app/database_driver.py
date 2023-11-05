from database import DataBase
from models import PredictedLoadModel
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

if __name__ == '__main__':
    # Create a database object
	db = DataBase()
	try:
		# Connect to the database
		db.connect()
		db.delete_collection("Wooster")
		db.models.delete_collection()
		# Create a collection for a node on the grid and inport the csv data
		db.create_collection("Wooster", "Wooster_Data")
		
		# Create a model for the node
		model = PredictedLoadModel(db, "Wooster")
		model.train()
  
		print("November 7, 2022")
		print(model.predict_weekly_loads(2022, 11, 7, 0))
  
		print("July 14, 2023")
		print(model.predict_weekly_loads(2023, 7, 14, 20))

		
	except Exception as e:
		print(e)
	finally:
		# db.delete_collection("Wooster")
		db.models.delete_collection()