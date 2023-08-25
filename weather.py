import requests
import os
import datetime
from dotenv import load_dotenv
from utils import date_str_to_date_instance

load_dotenv()
API_KEY = os.environ["API_KEY"]

def get_weather_forecast_data(city, date_str):
    """ returns data for one day like 
    [{'time': '2023-08-26 17:00', 'temp_c': 25.6, 'humidity': 61, 'wind_kph': 2.9, 'chance_of_rain': 0},
    {'time': '2023-08-26 18:00', 'temp_c': 23.9, 'humidity': 70, 'wind_kph': 4.7, 'chance_of_rain': 0}]
    """
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()
    current_hour =  current_datetime.hour
    forecast_date = date_str_to_date_instance(date_str)
    
    if forecast_date < current_date:
        raise ValueError("Forecasted date is already in past")
    if (forecast_date - current_date).days > 13:
        raise ValueError(f"Forecasted date is more than 13 days ahead")

    params = {
        "key":API_KEY,
        "q": city,
        "dt": date_str
    }
    response = requests.get("https://api.weatherapi.com/v1/forecast.json", params=params)
    json_response = response.json()
    day_forecast = json_response["forecast"]["forecastday"][0]
    
    result = []
    for hour_forecast in day_forecast["hour"]:
        hour = int(hour_forecast["time"].split(" ")[1].split(":")[0])    
        if forecast_date != current_date or current_hour <= hour:               
            result.append(hour_forecast)
    return result
   
def get_dict_with_weather_data_lists(weather_forecast_data):
    """ returns data for one day like 
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
        shortened_time = hour_data["time"].split(" ")[1]

        for key in result.keys():
            if key == "time":
                result[key].append(shortened_time)
            else:
                result[key].append(hour_data[key])
    return result
