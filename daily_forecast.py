# import required modules
import requests, json
import time

import global_datas
from moon_phase import moon_phase


#------------------------------------------------------------------------------
# Get daily forecast from OpenWeatherMap
#------------------------------------------------------------------------------
class get_daily_forecast () :
    """Get daily forecast from OpenWeatherMap"""

    def __init__(self, API_key, city_name) :
        complete_url = "https://api.openweathermap.org/data/2.5/weather?appid=" + API_key + "&q=" + city_name

        # Get daily forcast from OWM
        try :
            response = requests.get(complete_url)
        except Exception as error :
            print("{} connection error: {} ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), error))
            print("\n")

        owm_data = response.json()
        self.code = owm_data["cod"]

       # Check for errors
        match self.code:
            case 401:
                raise Exception("API key error")
            case 404:
                raise Exception("City not found")
            case 409:
                raise Exception("Too many requests / mn")
            case 400000:
                raise Exception("Subscription error")
            case 200:
                # Extract usefull data
                self.date_UNIX = owm_data["dt"]
                self.city = owm_data["name"]

                weather = owm_data["weather"]
                self.weather_description = weather[0]["description"]
                self.weather_condition = weather[0]["id"]

                main = owm_data["main"]
                self.temperature = main["temp"]
                self.temperature_min = main["temp_min"]
                self.temperature_max = main["temp_max"]
                self.pressure = main["pressure"]
                self.humidity = main["humidity"]
            case _:
                raise Exception("Unable to retrive data from OWM")

    def get_city (self) :
        """Get city name"""
        return self.city

    def get_description (self) :
        """Get weather description"""
        return self.weather_description

    def get_code (self) :
        """Get code"""
        return self.code

    def get_weather_condition (self) :
        """Get weather weather_condition. See https://openweathermap.org/weather-conditions"""
        if self.weather_condition in global_datas.night_icons :
            if not(int(time.strftime("%H", time.localtime(self.date_UNIX))) in range (7, 21)) :
              moon = moon_phase()
              self.weather_condition = self.weather_condition * 10 + moon.get_moon_phase()

        return self.weather_condition

    def get_date_UNIX (self) :
        """Get forcast date (UNIX)"""
        return self.date_UNIX

    def get_week_day (self) :
        """Get forcast week day"""
        return str(time.strftime("%A", time.localtime(self.date_UNIX)))

    def get_delta_time (self) :
        """Get delta between current time and forcast time in hours"""
        return str(time.gmtime(time.time() - self.date_UNIX)[3])

    def get_temperature_kelvin (self) :
        """Get the temperature (Kalvin)"""
        return self.temperature

    def get_temperature_min_kelvin (self) :
        """Get the min temperature (Kelvin)"""
        return self.temperature_min

    def get_temperature_max_kelvin (self) :
        """Get the max temperature (Kelvin)"""
        return self.temperature_max

    def get_temperature_celsius (self) :
        """Get the temperature (Celsius)"""
        return self.temperature - 273.15

    def get_temperature_min_celsius (self) :
        """Get the min temperature (Celsius)"""
        return self.temperature_min - 273.15

    def get_temperature_max_celsius (self) :
        """Get the max temperature (Celsius)"""
        return self.temperature_max - 273.15

    def get_pressure (self) :
        """Get the pressure (hPa)"""
        return self.pressure

    def get_humidity (self) :
        """Get forcast humidity (percent)"""
        return self.humidity

