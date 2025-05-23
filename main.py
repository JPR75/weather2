#! /usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
import time

import screen
import config

################################################################################
################################  Main  ########################################
################################################################################
if __name__ =="__main__" :

    # Wait for the OS to be ready before starting
    time.sleep(config.os_ready_wait)

    if len(config.towns_list) > 0 :
      try :
        main_windows = Tk()
        date_canvas = Canvas(main_windows, width = config.screen_dimension['width'], height = 90, bg = 'black' )
        date_canvas.grid(row = 0, column = 0, rowspan = 1, padx = 0, pady = 0)
        forecast_canvas = Canvas(main_windows, width = config.screen_dimension['width'], height = (config.screen_dimension['height'] - 90), bg = 'black' )
        forecast_canvas.grid(row = 1, column = 0, rowspan = 3, padx = 0, pady = 0)
      except Exception as error :
        print("*** Error while creating sreen; aborting\n")
        print(error)
        print("\n")
      else :
        screen.drawScreens(date_canvas, forecast_canvas)
        main_windows.mainloop()
    else :
      print("*** Error no town defined in config file; aborting\n")
      print("\n")

