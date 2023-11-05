import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Load your DataFrame with columns ["year", "month", "day", "hour", "temperature", "load_requirement"]
# Replace the following line with loading your actual data
data = pd.read_csv("your_data.csv")

# Convert the DataFrame to a time series
data["date"] = pd.to_datetime(data[["year", "month", "day", "hour"]])
ts = data.set_index("date")[["temperature", "load_requirement"]]

# Visualize the time series data
ts.plot(figsize=(12, 6))
plt.title("Temperature and Load Requirement Time Series")
plt.show()

# Decompose the time series to understand its trend and seasonality
decomposition = sm.tsa.seasonal_decompose(ts, model="additive")
fig = decomposition.plot()
plt.show()

# Perform a seasonal difference to remove seasonality
seasonal_diff = ts.diff(24)  # Assuming hourly data with a daily seasonality

# Check for stationarity using Augmented Dickey-Fuller test
adf_test = sm.tsa.adfuller(seasonal_diff.dropna()["load_requirement"])
print("ADF Statistic:", adf_test[0])
print("p-value:", adf_test[1])

# Determine the order of differencing (d) to make the load_requirement data stationary
d = 1

# Perform autocorrelation and partial autocorrelation plots to determine the order of AR and MA terms
fig, ax = plt.subplots(2, 1, figsize=(12, 8))
sm.graphics.tsa.plot_acf(seasonal_diff.dropna()["load_requirement"], lags=40, ax=ax[0])
sm.graphics.tsa.plot_pacf(seasonal_diff.dropna()["load_requirement"], lags=40, ax=ax[1])
plt.show()

# Determine the order of AR and MA terms
p = 1  # Order of the AutoRegressive (AR) component
q = 1  # Order of the Moving Average (MA) component

# Determine the seasonal order (P, D, Q, S)
P = 1  # Seasonal AR order
D = 1  # Seasonal differencing
Q = 1  # Seasonal MA order
S = 24  # Seasonal period (daily seasonality)

# Fit the SARIMA model
sarima_model = sm.tsa.SARIMAX(
    ts["load_requirement"],
    order=(p, d, q),
    seasonal_order=(P, D, Q, S),
    enforce_stationarity=False,
    enforce_invertibility=False,
)
sarima_results = sarima_model.fit()

# Forecast future load requirements based on temperature
forecast_steps = 24  # Number of steps to forecast (hours)
forecast_temperature = data["temperature"].tail(forecast_steps)  # Replace with actual temperature data
forecast = sarima_results.get_forecast(steps=forecast_steps, exog=forecast_temperature.values.reshape(-1, 1))

# Get forecasted values and confidence intervals
forecast_values = forecast.predicted_mean
forecast_ci = forecast.conf_int()

# Visualize the forecast
plt.figure(figsize=(12, 6))
plt.plot(ts["load_requirement"], label="Observed Load Requirement")
plt.plot(forecast_values, label="Forecasted Load Requirement", color="red")
plt.fill_between(
    forecast_ci.index,
    forecast_ci.iloc[:, 0],
    forecast_ci.iloc[:, 1],
    color="pink",
    alpha=0.3,
    label="Confidence Interval",
)
plt.xlabel("Date")
plt.ylabel("Load Requirement")
plt.title("Load Requirement Forecast")
plt.legend()
plt.show()