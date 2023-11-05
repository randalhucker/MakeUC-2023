from database import DataBase
from models import PredictedLoadModel

if __name__ == '__main__':
    # Create a database object
	db = DataBase()
	try:
		# Connect to the database
		db.connect()
		# Create a collection for a node on the grid and inport the csv data
		db.create_collection("Wooster", "Wooster_Data")
		
		# Create a model for the node
		model = PredictedLoadModel(db, "Wooster")
		model.train()
		
	except Exception as e:
		print(e)
	finally:
		db.delete_collection("Wooster")
		db.models.delete_collection()