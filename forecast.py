#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pyowm
import time
import datetime

import openweathermap_key
import config
import global_datas

#------------------------------------------------------------------------------
# Get forecast from OpenWeathermap
#------------------------------------------------------------------------------
class getForecats () :
  """Get forecast from OpenWeathermap"""
  next_update = 0.0

  def __init__(self) :
    self.owm = pyowm.OWM(API_key=openweathermap_key.key, language='en')  # You MUST provide a valid API key

  def check_update (self) :
    """Is it time to update the forecast?"""
    if getForecats.next_update < time.time() :
      self.download_forecasts()
      #if config.update_delay < 2.0 :
      #  config.update_delay = 2.0
      getForecats.next_update = time.time() + (config.update_delay * 3600.0)

  def download_forecasts (self) :
    """Download forecast from OpenWeatherMap"""
    forecast = [[True, "Connection Failed", ""],
      ["", 99997, 0, 0, 0, "", 0, False],
      ["", 99997, 0, 0, 0, "", 0, False],
      ["", 99997, 0, 0, 0, "", 0, False],
      ["", 99997, 0, 0, 0, "", 0, False],
      ["", 99997, 0, 0, 0, "", 0, False],
      ["", 99997, 0, 0, 0, "", 0, False]]
    global_datas.forecasts = []
    for town in config.towns_list :
      try :
        observation = self.owm.weather_at_place(town[0])
        fc = self.owm.three_hours_forecast(town[0])
        forecast[0][1] = observation.get_location().get_name()
      except Exception as error :
        forecast = [[True, "Connection Failed", ""],
          ["", 99997, 0, 0, 0, "", 0, False],
          ["", 99997, 0, 0, 0, "", 0, False],
          ["", 99997, 0, 0, 0, "", 0, False],
          ["", 99997, 0, 0, 0, "", 0, False],
          ["", 99997, 0, 0, 0, "", 0, False],
          ["", 99997, 0, 0, 0, "", 0, False]]
        global_datas.forecasts += [forecast[0] + forecast[1] + forecast[2] + forecast[3] + forecast[4] + forecast[5] + forecast[6]]
        print("Forcast exception : 1\n")
      else :
        forecast[0][0] = False  # Status = OK

        # For today lets get the status at now_offset (updated evry 3h by Openweathermap)
        date = datetime.datetime.today() + datetime.timedelta(hours = config.now_offset)
        try :
          f = fc.get_weather_at(date)
          forecast[0][2] = time.strftime("Forecast time: %H:%M GMT", time.gmtime(f.get_reference_time()))
          forecast[1][0] = f.get_detailed_status()
          forecast[1][1] = f.get_weather_code()
          forecast[1][2] = int(round(f.get_temperature('celsius')['temp'], 0))
          forecast[1][3] = int(round(f.get_temperature('celsius')['temp_max'], 0))
          forecast[1][4] = int(round(f.get_temperature('celsius')['temp_min'], 0))
          forecast[1][5] = time.strftime("%A", time.localtime(f.get_reference_time()))
          forecast[1][6] = time.gmtime(f.get_reference_time() - time.time())[3]
          forecast[1][7] = forecast[1][1] in global_datas.warning_states
        except Exception as error :
          forecast[1] = ["", 99997, 0, 0, 0, "", 0, False]
          print("Forcast exception : 2\n")

        # For today lets also get the status at now_later (updated evry 3h by Openweathermap)
        date = datetime.datetime.today() + datetime.timedelta(hours = config.now_later)
        try :
          f = fc.get_weather_at(date)
          forecast[2][0] = f.get_detailed_status()
          forecast[2][1] = f.get_weather_code()
          forecast[2][2] = int(round(f.get_temperature('celsius')['temp'], 0))
          forecast[2][3] = int(round(f.get_temperature('celsius')['temp_max'], 0))
          forecast[2][4] = int(round(f.get_temperature('celsius')['temp_min'], 0))
          forecast[2][5] = time.strftime("%A", time.localtime(f.get_reference_time()))
          forecast[2][6] = time.gmtime(f.get_reference_time() - time.time())[3]
          forecast[2][7] = forecast[2][1] in global_datas.warning_states
        except Exception as error :
          forecast[2] = ["", 99997, 0, 0, 0, "", 0, False]
          print("Forcast exception : 3\n")

        # For other days lets get the status and temperature for mid day
        for i in range(1, 5):
          date = datetime.datetime.today() + datetime.timedelta(days = i)
          date = date.replace(hour = 12, minute = 00, second = 00)
          try :
            f = fc.get_weather_at(date)
            forecast[i+2][0] = f.get_detailed_status()
            forecast[i+2][1] = f.get_weather_code()
            forecast[i+2][2] = int(round(f.get_temperature('celsius')['temp'], 0))
            forecast[i+2][3] = int(round(f.get_temperature('celsius')['temp_max'], 0))
            forecast[i+2][4] = int(round(f.get_temperature('celsius')['temp_min'], 0))
            forecast[i+2][5] = time.strftime("%A", time.localtime(f.get_reference_time()))
            forecast[i+2][6] = time.gmtime(f.get_reference_time() - time.time())[3]
            forecast[i+2][7] = forecast[i+2][1] in global_datas.warning_states
          except Exception as error :
            forecast[i+2] = ["", 99997, 0, 0, 0, "", 0, False]
            print("Forcast exception : 4\n")

        global_datas.forecasts += [forecast[0] + forecast[1] + forecast[2] + forecast[3] + forecast[4] + forecast[5] + forecast[6]]
