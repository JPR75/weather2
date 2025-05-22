#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime

from daily_forecast import get_daily_forecast
from five_days_forecast import get_five_days_forecast
from air_quality import get_air_quality
import openweathermap_key
import aqcinorg_key
import config
import global_datas

#------------------------------------------------------------------------------
# Get forecast from OpenWeathermap
#------------------------------------------------------------------------------
class getForecats () :
  """Get forecast from OpenWeathermap"""
  next_update = 0.0

  def check_update (self) :
    """Is it time to update the forecast?"""
    if getForecats.next_update < time.time() :
        try :
            self.download_forecasts()
        except Exception as error :
            print("Forcast exception : 1 ")
            print(error)
            print(time.strftime("%H:%M:%S - %A, %B %d %Y", time.localtime(getForecats.next_update)))
            print("\n")
        else :
            getForecats.next_update = time.time() + (config.update_delay * 3600.0)

  def download_forecasts (self) :
    """Download forecast from OpenWeatherMap"""
    forecast = [[True, "Connection Failed", ""],
      ["Unknown", 99997, 0, 0, 0, "", 0, False],
      ["Unknown", 99997, 0, 0, 0, "", 0, False],
      ["Unknown", 99997, 0, 0, 0, "", 0, False],
      ["Unknown", 99997, 0, 0, 0, "", 0, False],
      ["Unknown", 99997, 0, 0, 0, "", 0, False],
      ["Unknown", 99997, 0, 0, 0, "", 0, False],
      ["Unknown", 99997, 0, 0, 0, "", 0, False]]
    global_datas.forecasts = []
    for town in config.towns_list :
      try :
        fc = get_daily_forecast(openweathermap_key.key, town[0])
        forecast[0][1] = fc.get_city()
      except Exception as error :
        forecast = [[True, "Connection Failed", ""],
          ["Unknown", 99997, 0, 0, 0, "", 0, False],
          ["Unknown", 99997, 0, 0, 0, "", 0, False],
          ["Unknown", 99997, 0, 0, 0, "", 0, False],
          ["Unknown", 99997, 0, 0, 0, "", 0, False],
          ["Unknown", 99997, 0, 0, 0, "", 0, False],
          ["Unknown", 99997, 0, 0, 0, "", 0, False],
          ["Unknown", 99997, 0, 0, 0, "", 0, False]]
        global_datas.forecasts += [forecast[0] + forecast[1] + forecast[2] + forecast[3] + forecast[4] + forecast[5] + forecast[6] + forecast[7]]
        print("Forcast exception : 2 ")
        print(error)
        print("\n")

      else :
        forecast[0][0] = False  # Status = OK

        # For today lets get the status at now_offset (updated evry 3h by Openweathermap)
        try :
          forecast[0][2] = time.strftime("Forecast time: %H:%M GMT", time.gmtime(fc.get_date_UNIX()))
          forecast[1][0] = fc.get_description()
          forecast[1][1] = fc.get_weather_condition()
          forecast[1][2] = int(round(fc.get_temperature_celsius()))
          forecast[1][3] = int(round(fc.get_temperature_max_celsius()))
          forecast[1][4] = int(round(fc.get_temperature_min_celsius()))
          forecast[1][5] = time.strftime("%A", time.localtime(fc.get_date_UNIX()))
          forecast[1][6] = time.gmtime(fc.get_date_UNIX() - time.time())[3]
          forecast[1][7] = forecast[1][1] in global_datas.warning_states
        except Exception as error :
          forecast[1] = ["", 99997, 0, 0, 0, "", 0, False]
          print("Forcast exception : 3 ")
          print(error)
          print("\n")

        # Get air quality
        fc = get_air_quality(aqcinorg_key.key, town[0])
        try :
          forecast[2][0] = fc.get_description()
          forecast[2][1] = fc.get_aqi_condition()
          forecast[2][2] = 0.0
          forecast[2][3] = 0.0
          forecast[2][4] = 0.0
          forecast[2][5] = fc.get_week_day()[0]
          forecast[2][6] = time.gmtime(fc.get_date_UNIX() - time.time())[3]
          forecast[2][7] = forecast[2][1] in global_datas.aqi_warning_states
        except Exception as error :
          forecast[2] = ["", 99997, 0, 0, 0, "", 0, False]
          print("Forcast exception : 4 ")
          print(error)
          print("\n")

        # For other days lets get the status and temperature for mid day
        fc = get_five_days_forecast(openweathermap_key.key, town[0])
        for i in range(1, 6):
          try :
            forecast[i+2][0] = fc.get_description()[i - 1]
            forecast[i+2][1] = fc.get_weather_condition()[i - 1]
            forecast[i+2][2] = int(round(fc.get_temperature_celsius()[i - 1]))
            forecast[i+2][3] = 0.0
            forecast[i+2][4] = 0.0
            forecast[i+2][5] = fc.get_week_day()[i - 1]
            forecast[i+2][6] = fc.get_forecast_hour()[i - 1]
            forecast[i+2][7] = forecast[i+2][1] in global_datas.warning_states
          except Exception as error :
            forecast[i+2] = ["", 99997, 0, 0, 0, "", 0, False]
            print("Forcast exception : 5 ")
            print(error)
            print("\n")

        global_datas.forecasts += [forecast[0] + forecast[1] + forecast[2] + forecast[3] + forecast[4] + forecast[5] + forecast[6] + forecast[7]]
