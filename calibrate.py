#!/usr/bin/env python3
import ev3dev.ev3 as ev3

ls = ev3.ColorSensor(ev3.INPUT_4)
rs = ev3.ColorSensor(ev3.INPUT_1)


ls.mode = 'RGB-RAW'
ls.mode = 'RGB-RAW'

while(True):
	print(max(ls.raw), max(rs.raw))
