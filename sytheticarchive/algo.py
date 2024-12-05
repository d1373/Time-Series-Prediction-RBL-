import pymongo
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
import numpy as np
import math
import requests
import webbrowser


warnings.filterwarnings("ignore", category=Warning)
warnings.filterwarnings("ignore", category=FutureWarning)
# Step 1: Data Retrieval and Preprocessing
def retrieve_data():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["RBL"]
    collection = db["dustbin_entries"]
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))
    return df

def preprocess_data(df):
    # Preprocess the data if necessary
    return df

def split_data(df):
    train_size = int(len(df) * 0.8)
    train_data = df.iloc[:train_size]
    validation_data = df.iloc[train_size:]
    return train_data, validation_data

# Step 2: Model Training and Forecasting
def train_arima_model(train_data):
    model = ARIMA(train_data["Total_amount"].astype(float), order=(5, 1, 0))
    model_fit = model.fit()
    return model_fit

def forecast_values(model_fit, periods):
    forecast = model_fit.forecast(steps=periods)
    return forecast

# Step 3: Accuracy Evaluation
def evaluate_accuracy(actual_values, forecasted_values):
    mae = mean_absolute_error(actual_values, forecasted_values)
    rmse = mean_squared_error(actual_values, forecasted_values, squared=False)
    return mae, rmse

# Step 4: Repeat for Each Dustbin
def process_dustbins(dustbins_data):
    dustbin_data_dict = {}
    dustbins_data = dustbins_data.reset_index(drop=True)

    for i, group in dustbins_data.groupby("Dustbin_ID"):
        group = group.set_index("Date")
        train_data, validation_data = split_data(group)

        model_fit = train_arima_model(train_data)
        forecasted_values = forecast_values(model_fit, len(validation_data))
        dustbin_data_dict[i] = {
            "validation_data": validation_data,
            "forecasted_values": forecasted_values
        }

    return dustbin_data_dict

def main():
    df = retrieve_data()
    df = preprocess_data(df)

    results = process_dustbins(df)

    print("Forecasted Results:")
    estimated_times = []
    for dustbin_id, dustbin_data in results.items():
        forecasted_values = dustbin_data["forecasted_values"]
        validation_data = dustbin_data["validation_data"]

        print(f"Dustbin {dustbin_id}:")
        # print("\tForecasted Values:")
        # print(forecasted_values)
        # print("\tValidation Data:")
        # print(validation_data)

        actual_values = validation_data["Total_amount"].values
        mae, rmse = evaluate_accuracy(actual_values, forecasted_values)
        # print(f"\tMAE: {mae}")
        # print(f"\tRMSE: {rmse}")
        # forecast_values = 0
        forecast_value = 0
        i=0
        for value in forecasted_values:
            forecast_value = forecast_value + value
            i=i+1
        forecast_value = forecast_value/i
        forecast_value = 6 + (12 - (forecast_value / 100) * 12)  # Convert to time format
        hour = math.floor(forecast_value)
        minutes_decimal = forecast_value - hour
        minutes = round(minutes_decimal * 60)
        estimated_time = f"{int(hour):02d}:{int(minutes):02d}"
        estimated_times.append(estimated_time)
        print(f"\tEstimated Time: {estimated_time}")
    send_estimated_times(estimated_times)
    webbrowser.open('http://localhost:3000/')


def send_estimated_times(estimated_times):
    # API endpoint to send estimated times
    api_endpoint = "http://localhost:3000/api/estimated_times"
    payload = {"estimated_times": estimated_times}

    try:
        response = requests.post(api_endpoint, json=payload)
        if response.status_code == 200:
            print("Estimated times successfully sent.")
        else:
            print("Failed to send estimated times. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error occurred while sending estimated times:", e)


if __name__ == "__main__":
    main()
