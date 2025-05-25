# import required modules
import requests, json
import time

import global_datas


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
        self.forecast_hour = []

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
                # Now + 3h forecast
                today = True
                now_plus_3h = int(time.strftime("%H", time.localtime())) + 3
                if (now_plus_3h <= 3) :
                    today_now_plus_3h = "03:00:00"
                elif (now_plus_3h <= 6) :
                    today_now_plus_3h = "06:00:00"
                elif (now_plus_3h <= 9) :
                    today_now_plus_3h = "09:00:00"
                elif (now_plus_3h <= 12) :
                    today_now_plus_3h = "12:00:00"
                elif (now_plus_3h <= 15) :
                    today_now_plus_3h = "15:00:00"
                elif (now_plus_3h <= 18) :
                    today_now_plus_3h = "18:00:00"
                elif (now_plus_3h <= 21) :
                    today_now_plus_3h = "21:00:00"
                else :
                    today_now_plus_3h = "03:00:00"
                    today = False

                # Extract usefull data
                self.city = owm_data["city"]["name"]
                self.date_UNIX = owm_data["list"][0]["dt"]
                for entry in owm_data["list"]:
                    date = entry["dt_txt"].split(" ")[0]
                    hour = entry["dt_txt"].split(" ")[1]
                    # if the current hour is between 00:00:00 and 19:00:00, then the current hour + 3h
                    # forecast is displayed
                    if (date == time.strftime("%Y-%m-%d", time.localtime()) and today == True) :
                        if (hour == today_now_plus_3h) :
                            self.weather_description.append(entry["weather"][0]["main"])
                            self.week_day.append(time.strftime("%A", time.localtime(entry["dt"])))
                            self.temperature.append(entry["main"]["temp"])
                            self.temperature_celsius.append(entry["main"]["temp"] - 273.15)
                            self.weather_condition.append(entry["weather"][0]["id"])
                            self.forecast_hour.append(hour)
                    if (date != time.strftime("%Y-%m-%d", time.localtime())) :
                        # if the current hour is between 19:00:00 and 00:00:00, then the tomorrow 3 AM
                        # forecast is displayed
                        if (today == False) :
                            if (hour == today_now_plus_3h) :
                                self.weather_description.append(entry["weather"][0]["main"])
                                self.week_day.append(time.strftime("%A", time.localtime(entry["dt"])))
                                self.temperature.append(entry["main"]["temp"])
                                self.temperature_celsius.append(entry["main"]["temp"] - 273.15)
                                self.weather_condition.append(entry["weather"][0]["id"])
                                self.forecast_hour.append(hour)
                                today = True
                        if (hour == "12:00:00") :
                            self.weather_description.append(entry["weather"][0]["main"])
                            self.week_day.append(time.strftime("%A", time.localtime(entry["dt"])))
                            self.temperature.append(entry["main"]["temp"])
                            self.temperature_celsius.append(entry["main"]["temp"] - 273.15)
                            self.weather_condition.append(entry["weather"][0]["id"])
                            self.forecast_hour.append(hour)
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
        if self.weather_condition[0] in global_datas.night_icons :
            if not(self.forecast_hour[0].split(":")[0] in range (7, 20)) :
              self.weather_condition[0] += "n"

        return self.weather_condition

    def get_date_UNIX (self) :
        """Get forcast date (UNIX)"""
        return self.date_UNIX

    def get_forecast_hour (self) :
        """Get forcast hour"""
        return self.forecast_hour

    def get_week_day (self) :
        """Get forcast week day"""
        return self.week_day

    def get_delta_time (self) :
        """Get delta between current time and forcast time in hours"""
        return str(time.gmtime(time.time() - self.date_UNIX)[3])

    def get_temperature_kelvin (self) :
        """Get the temperature (Kalvin)"""
        return self.temperature

    def get_temperature_celsius (self) :
        """Get the temperature (Celsius)"""
        return self.temperature_celsius

