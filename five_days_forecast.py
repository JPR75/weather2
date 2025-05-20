# import required modules
import requests, json
import time


#------------------------------------------------------------------------------
# Get daily forecast from OpenWeatherMap
#------------------------------------------------------------------------------
class get_five_days_forecast () :
    """Get daily forecast from OpenWeatherMap"""

    def __init__(self, API_key, city_name) :
        base_url = "http://api.openweathermap.org/data/2.5/forecast?"
        complete_url = base_url + "appid=" + API_key  + "&q=" + city_name

        # Get daily forcast from OWM
        response = requests.get(complete_url)
        owm_data = response.json()
        self.code = owm_data["cod"]

        self.weather_description = []
        self.weather_condition = []
        self.temperature = []
        self.temperature_celsius = []
        self.week_day = []

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
            case "200":
                # Extract usefull data
                self.city = owm_data["city"]["name"]
                self.date_UNIX = owm_data["list"][0]["dt"]
                for entry in owm_data["list"]:
                    self.date = entry["dt_txt"].split(" ")[0]
                    hour = entry["dt_txt"].split(" ")[1]
                    if (self.date != time.strftime("%Y-%m-%d", time.localtime())) :
                        if (hour == "12:00:00") :
                            self.weather_description.append(entry["weather"][0]["main"])
                            self.week_day.append(time.strftime("%A", time.localtime(entry["dt"])))
                            self.temperature.append(entry["main"]["temp"])
                            self.temperature_celsius.append(entry["main"]["temp"] - 273.15)
                            self.weather_condition.append(entry["weather"][0]["id"])
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
        return self.weather_condition

    def get_date_UNIX (self) :
        """Get forcast date (UNIX)"""
        return self.date_UNIX

    def get_week_day (self) :
        """Get forcast week day"""
        return self.week_day

    def get_delta_time (self) :
        """Get delta between current time and forcast time in hours"""
        print(time.time())
        print(self.date_UNIX)
        return str(time.gmtime(time.time() - self.date_UNIX)[3])

    def get_temperature_kelvin (self) :
        """Get the temperature (Kalvin)"""
        return self.temperature

    def get_temperature_celsius (self) :
        """Get the temperature (Celsius)"""
        return self.temperature_celsius

