#! /usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
import time

import forecast
import config
import global_datas

#------------------------------------------------------------------------------
# Update time and date
#------------------------------------------------------------------------------
class updateDateScreen (Canvas) :
  """Update time and date"""
  def __init__(self, date_canvas) :
    self.canvas = date_canvas

  def update_date (self) :
    try :
      # Hour and date
      hour = time.strftime("%H:%M:%S - %A, %B %d %Y", time.localtime())
      self.canvas.create_text(config.horizontal_offset + 230, 0, anchor = NW, fill = "white", font = ("Arial", 32), text = hour, width = 0)
    except Exception as error :
      print("Screen exception : 1\n")
      raise

#------------------------------------------------------------------------------
# Update the today screen with current info
#------------------------------------------------------------------------------
class updateTodayScreen (Canvas) :
  """Update the today screen with current info"""
  def __init__(self, main_canvas) :
    self.canvas = main_canvas
    self.canvas.icon_forcast = []
    self.canvas.icon_network_disconnect = []
    self.canvas.icon_danger = []

  def update_today (self, forcast_data) :
    # Town name
    self.canvas.create_text(config.horizontal_offset + 40, 0, anchor = NW, fill = "white", font = ("Arial", 64), text = forcast_data[1], width = 0)

    for i in range(0, 2) :
      index = i * 8
      horizotal_align = i * 512 + config.horizontal_offset

      # State icon
      try :
        self.canvas.icon_forcast.append(PhotoImage(file = 'icons/' + str(forcast_data[4 + index]) + '.gif'))
      except Exception as error :
        error_text = 'Icon error: ' + str(forcast_data[4 + index]) + '.gif'
        self.canvas.create_text(horizotal_align + 60, 95, anchor = NW, fill = "white", font = ("Arial", 32), text = error_text, width = 0)
        print("Screen exception : 2\n")
        raise
      else :
        self.canvas.create_image(horizotal_align + 60, 95, anchor = NW, image = self.canvas.icon_forcast[i])

      try :
        # Status
        self.canvas.create_text(horizotal_align + 230, 100, anchor = NW, fill = "white", font = ("Arial", 32), text = forcast_data[3 + index], width = 0)

        # Temperature
        T = 'T = ' + str(forcast_data[5 + index]) + config.unit
        self.canvas.create_text(horizotal_align + 230, 150, anchor = NW, fill = "white", font = ("Arial", 32), text = T, width = 0)

        # Forcast time from now in hour
        time_offset = 'now + ' + str(forcast_data[9 + index]) + 'h'
        self.canvas.create_text(horizotal_align + 230, 200, anchor = NW, fill = "white", font = ("Arial", 32), text = time_offset, width = 0)

        if forcast_data[10 + index] == True :
          self.canvas.create_text(50 + horizotal_align, 220, anchor = NW, fill = "red", font = ("Arial", 28), text = "Warning!", width = 0)
      except Exception as error :
        print("Screen exception : 3\n")
        raise

#------------------------------------------------------------------------------
# Update the forecast screens with current info
#------------------------------------------------------------------------------
class updateForcatScreen (Canvas) :
  """Update the forecast screens with current info"""
  def __init__(self, main_canvas) :
    self.canvas = main_canvas
    self.canvas.icon_forcast_data = []

  def update_forecasts (self, forcast_data) :
    for i in range(0, 4):
      index = i * 8
      horizotal_align = i * 256 + config.horizontal_offset

      # Day
      self.canvas.create_text(40 + horizotal_align, 270, anchor = NW, fill = "white", font = ("Arial", 28), text = forcast_data[24 + index], width = 0)

      # Icon
      try :
        self.canvas.icon_forcast_data.append(PhotoImage(file = 'icons/' + str(forcast_data[20 + index]) + '.gif'))
      except Exception as error :
        error_text = 'Icon error: ' + str(forcast_data[20 + index]) + '.gif'
        self.canvas.create_text(horizotal_align + 57, 315, anchor = NW, fill = "white", font = ("Arial", 32), text = error_text, width = 0)
        print("Screen exception : 4\n")
        raise
      else :
        self.canvas.create_image(57 + horizotal_align, 315, anchor = NW, image = self.canvas.icon_forcast_data[i])

      try :
        # Temperature
        T = 'T = ' + str(forcast_data[21 + index]) + config.unit
        self.canvas.create_text(50 + horizotal_align, 450, anchor = NW, fill = "white", font = ("Arial", 28), text = T, width = 0)

        # Warning
        if forcast_data[26 + index] == True :
          self.canvas.create_text(50 + horizotal_align, 490, anchor = NW, fill = "red", font = ("Arial", 28), text = "Warning!", width = 0)
      except Exception as error :
        print("Screen exception : 5\n")
        raise


#------------------------------------------------------------------------------
# Draw screens
#------------------------------------------------------------------------------
class drawScreens (Canvas) :
  """Draw screens"""
  delay = 0.0

  def __init__(self, date_canvas, forecast_canvas) :
    Frame.__init__(self)
    self.date_canvas = date_canvas
    self.forecast_canvas = forecast_canvas

    self.index = 0
    self.refresh_screen()

  def refresh_screen (self) :
    """Refresh the screen"""
    self.date_canvas.delete("all")
    try :
      updateDateScreen(self.date_canvas).update_date()
    except Exception as error :
      print("Screen exception : 6\n")

    if self.index == 0 :
      forecast.getForecats().check_update()
#    print("datas : {}\n".format(global_datas.forecasts))
#    print("len = {}\n".format(len(global_datas.forecasts)))
#    print("index out : {}\n".format(self.index))

    if len(global_datas.forecasts) > 0 :
      if drawScreens.delay < time.time() :
#        print("index in : {}\n".format(self.index))
        forcast_data = global_datas.forecasts[self.index]
        drawScreens.delay = time.time() + config.towns_list[self.index][1]

        try :
          self.forecast_canvas.delete("all")
          updateTodayScreen(self.forecast_canvas).update_today(forcast_data)
          updateForcatScreen(self.forecast_canvas).update_forecasts(forcast_data)
        except Exception as error :
          print("Screen exception : 7\n")

        if self.index < len(global_datas.forecasts) - 1 :
          self.index += 1
        else :
          self.index = 0

    self.after(500, self.refresh_screen)
