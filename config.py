#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Towns id, see http://openweathermap.org/help/city_list.txt
# (town id , number of seconds the town weather is shown befor switching to the next)
# towns_list = [('Paris' , 10), ('Stockholm' , 10)]
# towns_list = [('Paris' , 60), ('Stockholm' , 10), ('New York' , 10)]
# towns_list = [('Paris' , 10)]
towns_list = [('Paris', 10), ('Stockholm', 10)]

# Frequency at which Openweathermap will be checked (in hour)
# 2.0 = 2h
# 0.5 = 30 minutes
update_delay = 0.5

# Wait for OS be ready before lanching the software.
# Can be useful if the OS take times to connect to the wifi
# Time in seconds
os_ready_wait = 0

#Screen dimensions
screen_dimension = {'width' : 1270, 'height' : 700}

# Horizontal offset in pixels
horizontal_offset = 5

# Temperature unit
unit = " C"

