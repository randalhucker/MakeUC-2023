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

pd.set_option("display.max_rows", 50)  # Display up to 20 rows


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
        self.sequence_length = 2496  # 2 years * 52 weeks * 24 hours
        # Normalize the data using Min-Max scaling
        try:
            model_return = self.database.models.get_model(col_name)
            self.scaler: MinMaxScaler = pickle.loads(model_return["scaler"])
            self.model = pickle.loads(model_return["model"])
        except Exception as e:
            self.model = None
            self.scaler = MinMaxScaler()
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
        data.drop(["_id"], axis=1, inplace=True)

        # Collapse the data into weekly averages
        self.data = self.collapse_dataset(data)

    # This method is used to train the model
    # The model is trained using the data currently stored in the data attribute
    # The model is then saved to / updated in the database
    def train(self):
        # Format the data (import from database and collapse into weekly averages)
        self.format_data()

        data_scaled = self.scaler.fit_transform(self.data)

        # Create sequences for input data
        # Sequence length is how far back the model considers to produce a single prediction
        X, y = [], []

        for i in range(self.sequence_length, len(self.data)):
            X.append(
                data_scaled[i - self.sequence_length : i, :]
            )  # X contains all the features except the target variable (this might need to be sequence_length - i: i)
            y.append(data_scaled[i, -1])  # 'load requirement' is the target variable

        X, y = np.array(X), np.array(y)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Build the LSTM model
        model = Sequential()
        model.add(
            LSTM(
                units=50,
                activation="relu",
                input_shape=(X_train.shape[1], X_train.shape[2]),
            )
        )
        model.add(Dense(units=1))  # Output layer

        # Compile the model
        model.compile(optimizer="adam", loss="mean_squared_error")

        # Train the model
        model.fit(X_train, y_train, epochs=1, batch_size=32)

        # Save the new model to the class and update the database
        self.model = model
        self.database.models.upload_model(
            self.collection_name, pickle.dumps(model), pickle.dumps(self.scaler)
        )

        # Evaluate the model and print the results
        print(model.evaluate(X_test, y_test))

    # This method is used to predict the estimated load requirement for a given node in the grid for a given week
    # This method will return a pandas dataframe containing the predicted load requirement for each hour (averaged for the given week)
    # This method will use the current model to make the prediction, if no model is present it will return None
    # if updated predictions are required, the format data and train methods should be called first
    def predict_weekly_loads(
        self, year: int, month: int, day: int, average_temperature: float
    ) -> pd.DataFrame:
        # Create a dataframe in the format of the collapsed dataset
        df = pd.DataFrame(
            columns=[
                "year",
                "month",
                "week",
                "hour",
                "average_temperature",
                "average_load_requirement",
            ]
        )
        # Get the week number for the given date
        week = datetime(year, month, day).isocalendar()[1]

        # Get starting index for the week
        start_index = self.data["year": year, "week": week].index[-1]

        # Ensure data is scaled and transformed
        scaled_df = self.scaler.transform(df)

        # Create sequences for input data
        # Sequence length is how far back the model considers to produce a single prediction
        X = []
        X.append(scaled_df[start_index - self.sequence_length : start_index, :])
        X = np.array(X)

        # Make a prediction for the expected load requirement for each hour averaged over the week
        predictions = self.model.predict(X)
        # Update the 'average_load_requirement' column with predictions
        df["average_load_requirement"] = predictions
        # Inverse transform the scaled columns
        prediction_df = self.scaler.inverse_transform(df)

        return prediction_df

    # This method is used to collapse the dataset into weekly averages
    # This method will return a pandas dataframe containing the collapsed data
    def collapse_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        # Ensure that the 'day' column is in datetime format
        df["day"] = pd.to_datetime(df[["year", "month", "day"]])
        # Transform the 'day' column to week number
        df["day"] = df["day"].apply(lambda x: x.isocalendar()[1])

        print(df)

        # Collapse the dataset into weekly averages
        collapsed_df = df.groupby(["year", "month", "day", "hour"]).mean().reset_index()

        print(collapsed_df.iloc[0:50])

        # Rename columns to match the desired output
        collapsed_df.columns = [
            "year",
            "month",
            "week",
            "hour",
            "average_temperature",
            "average_load_requirement",
        ]
        return collapsed_df.astype(
            {
                "year": int,
                "month": int,
                "week": int,
                "hour": int,
                "average_temperature": float,
                "average_load_requirement": float,
            }
        )
