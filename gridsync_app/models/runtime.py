
import pandas as pd
import numpy as np
import pickle
from database import DataBase
from collection import Collection as col
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense
from datetime import datetime, timedelta

# Model class
# This class is used to train and predict using a Long Short Term Memory (LSTM) Recurrent Neural Network (RNN)
class PredictedLoadModel:
    def __init__(self, db: DataBase, col_name: str):
        # The model ID is used to identify the model in the database, this ID will match the ID of a node in the grid for which we have records
        self.collection_name = col_name
        # The collection attribute is used to interact with the collection in the database
        self.collection = db.get_collection(col_name)
        # The database class is used to interact with MongoDB
        self.database: DataBase = db
        # The sequence length is the number of data points that the model will consider to make a prediction (2 years worth of data once records are collapsed)
        self.sequence_length = 2496 # 2 years * 52 weeks * 24 hours 
        # The model attribute will be used to store the model (if one is present in the database)
        try:
            self.model = pickle.loads(self.database.models.get_model(col_name))
        except Exception as e:
            self.model = None
        # The data attribute will be used to store the data used to train / retrain the model
        self.data: pd.DataFrame = None
    
    # This method is used to format the data for the model
    # it uses the database class to interact with MongoDB and retrieve the data
    # it then formats the data into a pandas dataframe and collapses the data into a weekly average
    # that can be used to train the model
    def format_data(self) -> None:
        # Load data from collection
        data: pd.DataFrame = self.collection.get_records()
        
        # Select relevant columns
        data.drop(['_id'], axis=1, inplace=True)
       
        # Collapse the data into weekly averages
        self.data = self.collapse_dataset(data)

    # This method is used to train the model
    # The model is trained using the data currently stored in the data attribute 
    # The model is then saved to / updated in the database
    def train(self):
        # Format the data (import from database and collapse into weekly averages)
        self.format_data()
        # Normalize the data using Min-Max scaling
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(self.data)

        # Create sequences for input data
        # Sequence length is how far back the model considers to produce a single prediction
        X, y = [], []

        for i in range(self.sequence_length, len(self.data)):
            X.append(data_scaled[i - self.sequence_length:i, :]) # X contains all the features except the target variable (this might need to be sequence_length - i: i)
            y.append(data_scaled[i, -1])  # 'load requirement' is the target variable

        X, y = np.array(X), np.array(y)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Build the LSTM model
        model = Sequential()
        model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))
        model.add(Dense(units=1))  # Output layer

        # Compile the model
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train the model
        model.fit(X_train, y_train, epochs=50, batch_size=32)

        # Save the new model to the class and update the database
        self.model = model
        self.database.models.upload_model(self.collection_name, pickle.dumps(model))
        
        # Evaluate the model and print the results
        print(model.evaluate(X_test, y_test))

    # This method is used to predict the estimated load requirement for a given node in the grid for a given week
    # This method will return a pandas dataframe containing the predicted load requirement for each hour (averaged for the given week)
    # This method will use the cureent model to make the prediction, if no model is present it will return None
    # if updated predictions are required, the format data and train methods should be called first
    def predict_weekly_loads(self, year, month, week, average_temperature):
        # Create a dataframe in the format of the collapsed dataset
        df = pd.DataFrame(columns=["year", "month", "week", "hour", "average_temperature"])
        for hour in range(24):
            # Append row to the DataFrame
            df = df.append({"year": year, "month": month, "week": week, "hour": hour, "average_temperature": average_temperature}, ignore_index=True)
        # Make a prediction for the expected load requirement for each hour averaged over the week
        predictions = self.model.predict(df)
        df['average_load_prediction'] = predictions
        return df
    
    # This method is used to collapse the dataset into weekly averages
    # This method will return a pandas dataframe containing the collapsed data
    def collapse_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        # Ensure that the 'day' column is in datetime format
        df['day'] = pd.to_datetime(df[['year', 'month', 'day']])
        # Group the data by year, week, and hour, and calculate the mean values for temperature and load_requirement
        collapsed_df = df.groupby([df['year'], df['month'], pd.Grouper(key='day', freq='W'), df['hour']])[['temperature', 'load_requirement']].mean().reset_index()
        # Rename columns to match the desired output
        collapsed_df.columns = ['year', 'month', 'day', 'hour', 'average_temperature', 'average_load_requirement']
        return collapsed_df.astype({'year': int, 'month': int, 'day': int, 'hour': int, 'average_temperature': float, 'average_load_requirement': float})