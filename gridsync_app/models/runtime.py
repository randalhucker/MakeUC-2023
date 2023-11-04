
import pandas as pd
import numpy as np
import pickle
from database import Database as db
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Model class
# This class is used to train and predict using a Long Short Term Memory (LSTM) Recurrent Neural Network (RNN)
class PredictedLoadModel:
    def __init__(self, ModelID):
        self.id = ModelID
        self.database = db.DataBase()
        self.model = pickle.loads(self.database.get_model(ModelID))

    def train(self):
        # Load historical data
        data = self.database.get_records(self.id)

        data = self.collapse_dataset(data)

        # Data preprocessing
        # Data contains columns: 'year', 'month', 'season', 'day', 'hour', 'temperature', 'load_requirement'

        # Select relevant columns
        selected_features = ['year', 'month', 'season', 'day', 'hour', 'temperature', 'load_requirement']
        data = data[selected_features]

        # Normalize the data using Min-Max scaling
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)

        # Create sequences for input data (e.g., look back 24 hours for predictions)
        # Sequence length is how far back the model considers to produce a single prediction
        # in the current case, the model will look back 24 hours to predict the load requirement for the next hour (24 * 7 features to get the )
        sequence_length = 24 
        X, y = [], []

        for i in range(sequence_length, len(data)):
            X.append(data_scaled[i - sequence_length:i, :]) # X contains all the features except the target variable (this might need to be sequence_length - i: i)
            y.append(data_scaled[i, -1])  # 'load_requirement' is the target variable

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
        self.model = model


    def collapse_dataset(self, df):
        # Ensure that the 'day' column is in datetime format
        df['day'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-' + df['day'].astype(str), format='%Y-%m-%d')

        # Group the data by year, week, and hour, and calculate the mean values for temperature and load_requirement
        collapsed_df = df.groupby([df['year'], df['month'], df['day'].dt.week, df['hour']])[['temperature', 'load_requirement']].mean().reset_index()

        # Rename columns to match the desired output
        collapsed_df.columns = ['year', 'month', 'week', 'hour', 'average_temperature', 'average_load_requirement']

        return collapsed_df


    def predict(self):
        pass