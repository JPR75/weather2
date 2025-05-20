# import required modules
import requests, json
import time

import config


#------------------------------------------------------------------------------
# Get daily forecast from aqcin.org
#------------------------------------------------------------------------------
class get_air_quality () :
    """Get daily forecast from aqcin.org"""

    def __init__(self, API_key, city_name) :
        base_url = "https://api.waqi.info/feed/"
        complete_url = base_url + city_name + "/?token=" + API_key

        # Get daily forcast from aqcin.org
        response = requests.get(complete_url)
        aqicn_data = response.json()
        self.code = aqicn_data["status"]

       # Check for errors
        match self.code:
            case "ok":
                # Extract usefull data
                self.date_UNIX = aqicn_data["data"]["time"]["v"]
                self.city = aqicn_data["data"]["city"]["name"]
                self.air_quality = aqicn_data["data"]["aqi"]

                self.iaqi = aqicn_data["data"]["iaqi"]

                # Not all locations have this data available
#                self.iaqi_co = self.iaqi["co"]["v"]
#                self.iaqi_h = self.iaqi["h"]["v"]
#                self.iaqi_no2 = self.iaqi["no2"]["v"]
#                self.iaqi_o3 = self.iaqi["o3"]["v"]
#                self.iaqi_p = self.iaqi["p"]["v"]
#                self.iaqi_pm10 = self.iaqi["pm10"]["v"]
#                self.iaqi_pm25 = self.iaqi["pm25"]["v"]
#                self.iaqi_so2 = self.iaqi["so2"]["v"]
#                self.iaqi_t = self.iaqi["t"]["v"]
#                self.iaqi_w = self.iaqi["w"]["v"]
            case _:
                raise Exception("Unable to retrive data from aqcin.org")

    def get_city (self) :
        """Get city name"""
        return self.city

    def get_code (self) :
        """Get code"""
        return self.code

    def get_aqi (self) :
        """Get air quality. See https://aqicn.org/api/"""
        return self.air_quality

    def get_description (self) :
        """Get air quality description. See See https://aqicn.org/api/"""
        if self.air_quality < 51 :
            aqi_description = "Good"
        elif self.air_quality < 101 :
            aqi_description = "Moderate"
        elif self.air_quality < 151 :
            aqi_description = "Bad"
        elif self.air_quality < 201 :
            aqi_description = "Unhealthy"
        elif self.air_quality < 301 :
            aqi_description = "Very unhealthy"
        elif self.air_quality > 300 :
            aqi_description = "Hazardous"
        else :
            aqi_description = "Unknown"

        return aqi_description

    def get_aqi_condition (self) :
        """Get air quality condition. See See https://aqicn.org/api/"""
        if self.air_quality < 51 :
            aqi_condition = 0 # Good
        elif self.air_quality < 101 :
            aqi_condition = 1 # Moderate
        elif self.air_quality < 151 :
            aqi_condition = 2 # Bad
        elif self.air_quality < 201 :
            aqi_condition = 3 # Unhealthy
        elif self.air_quality < 301 :
            aqi_condition = 4 # Very nhealthy
        elif self.air_quality > 300 :
            aqi_condition = 5 # Hazardous
        else :
            aqi_condition = 99997 # Unknown

        return aqi_condition

    def get_date_UNIX (self) :
        """Get forcast date (UNIX)"""
        return self.date_UNIX

    def get_week_day (self) :
        """Get forcast week day"""
        return str(time.strftime("%A", time.localtime(self.date_UNIX)))

    def get_delta_time (self) :
        """Get delta between current time and forcast time in hours"""
        return str(time.gmtime(time.time() - self.date_UNIX)[3])

# Not all locations have this data available
#    def get_co (self) :
#        """Get co"""
#        return self.iaqi_co
#
#    def get_h (self) :
#        """Get h"""
#        return self.iaqi_h
#
#    def get_no2 (self) :
#        """Get no2"""
#        return self.iaqi_no2
#
#    def get_o3 (self) :
#        """Get o3"""
#        return self.iaqi_o3
#
#    def get_p (self) :
#        """Get p"""
#        return self.iaqi_p
#
#    def get_pm10 (self) :
#        """Get pm10"""
#        return self.iaqi_pm10
#
#    def get_pm25 (self) :
#        """Get pm25"""
#        return self.iaqi_pm25
#
#    def get_so2 (self) :
#        """Get so2"""
#        return self.iaqi_so2
#
#    def get_t (self) :
#        """Get t"""
#        return self.iaqi_t
#
#    def get_w (self) :
#        """Get w"""
#        return self.iaqi_w

