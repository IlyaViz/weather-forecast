import matplotlib.pyplot as plt 
from weather import get_weather_forecast_data, get_dict_with_weather_data_lists

if __name__ == "__main__":
    city = input("City? \n")
    date_str = input("Date? (format example: 2023-08-15). Max forecast is 13 days ahead \n")

    weather_forecast_data = get_weather_forecast_data(city, date_str)
    dict_with_weather_data_lists = get_dict_with_weather_data_lists(weather_forecast_data)

    time_list = dict_with_weather_data_lists["time"]
    temp_c_list = dict_with_weather_data_lists["temp_c"]
    humidity_list = dict_with_weather_data_lists["humidity"]
    wind_kph_list = dict_with_weather_data_lists["wind_kph"]
    chance_of_rain_list = dict_with_weather_data_lists["chance_of_rain"]

    figure, axis = plt.subplots(4, 1)
    figure.tight_layout(pad=0.6, h_pad=0.5)
    figure.suptitle(f"{city} {date_str}", color="red")

    axis[0].plot(time_list, temp_c_list)
    axis[0].set_ylabel("Temperature (°C)")

    axis[1].plot(time_list, humidity_list)
    axis[1].set_ylabel("Humidity (%)")
    
    axis[2].plot(time_list, wind_kph_list)
    axis[2].set_ylabel("Wind (kph)")
    
    axis[3].plot(time_list, chance_of_rain_list)
    axis[3].set_ylabel("Chance of rain (%)")

    plt.show()

