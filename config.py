#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Towns id, see http://openweathermap.org/help/city_list.txt
# (town id , number of seconds the town weather is shown befor switching to the next)
#towns_list = [('Stockholm,se' , 3), ('@,@' , 3), ('Shiraz,ir' , 3)]
#towns_list = [('@,@' , 3), ('@,@' , 3), ('@,@' , 3)]
#towns_list = [('Paris,fr' , 3), ('Stockholm,se' , 3), ('Shiraz,ir' , 3), ('New York,us' , 3), ('Pyaozerskiy,ru' , 3)]
towns_list = [('Paris,fr' , 60), ('Lund,se' , 10)]

# Frequency at which Openweathermap will be cheked (in hour)
# 2.0 = 2h
update_delay = 2.0

# Weather at now + this delay (in hour)
# 4 = 4h
now_offset = 1
now_later = 4

#Screen dimensions
screen_dimension = {'width' : 1270, 'height' : 700}

# Horizontal offset in pixels
horizontal_offset = 5

# Temperature unit
unit = " C"

