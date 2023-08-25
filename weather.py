import requests
import os
import datetime
from dotenv import load_dotenv
from utils import date_str_to_date_instance

load_dotenv()
API_KEY = os.environ["API_KEY"]

def get_weather_forecast_data(city, date_str):
    """ returns data like 
    [{'time': '2023-08-26 17:00', 'temp_c': 25.6, 'humidity': 61, 'wind_kph': 2.9, 'chance_of_rain': 0},
    {'time': '2023-08-26 18:00', 'temp_c': 23.9, 'humidity': 70, 'wind_kph': 4.7, 'chance_of_rain': 0}]
    """
    forecast_date = date_str_to_date_instance(date_str)
    if forecast_date < datetime.datetime.now().date():
        raise ValueError("Forecasted date is already in past")

    params = {
        "key":API_KEY,
        "q": city,
        "days": 14
    }
    response = requests.get("https://api.weatherapi.com/v1/forecast.json", params=params)
    json_response = response.json()
    days_forecast = json_response["forecast"]["forecastday"]
    
    result = []
    for day_forecast in days_forecast:
        date = date_str_to_date_instance(day_forecast["date"])
        if forecast_date == date:
            for hourly_forecast in day_forecast["hour"]:
                temp_result = {}

                hour = int(hourly_forecast["time"].split(" ")[1].split(":")[0])    
                current_datetime = datetime.datetime.now()
                if forecast_date != current_datetime.date() or current_datetime.hour <= hour:               
                    temp_result["time"] = hourly_forecast["time"]
                    temp_result["temp_c"] = hourly_forecast["temp_c"]
                    temp_result["humidity"] = hourly_forecast["humidity"]
                    temp_result["wind_kph"] = hourly_forecast["wind_kph"]
                    temp_result["chance_of_rain"] = hourly_forecast["chance_of_rain"]
                    result.append(temp_result)
            break

    return result
   
def get_dict_with_weather_data_lists(weather_forecast_data):
    """ returns data like 
    {'time': ['17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'], 
    'temp_c': [25.6, 23.9, 21.8, 20.9, 20.5, 20.2, 19.2], 
    'humidity': [61, 70, 76, 79, 81, 82, 87], 
    'wind_kph': [2.9, 4.7, 7.2, 9.4, 7.9, 10.8, 5.0], 
    'chance_of_rain': [0, 0, 0, 0, 70, 78, 86]} 
    """
    result = {
        "time": [],
        "temp_c": [],
        "humidity": [],
        "wind_kph": [],
        "chance_of_rain": []
    }
    for hour_data in weather_forecast_data:
        time = hour_data["time"].split(" ")[1]

        result["time"].append(time)
        result["temp_c"].append(hour_data["temp_c"])
        result["humidity"].append(hour_data["humidity"])
        result["wind_kph"].append(hour_data["wind_kph"])
        result["chance_of_rain"].append(hour_data["chance_of_rain"])
    return result
