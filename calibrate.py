#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from transporter import turn_back, turn_90,is_main_trail
from ev3dev2.motor import MediumMotor, LargeMotor, MoveTank
from time import sleep

ls = ev3.ColorSensor(ev3.INPUT_4)
rs = ev3.ColorSensor(ev3.INPUT_1)
tank =  MoveTank('outD', 'outA')

ls.mode = 'RGB-RAW'
ls.mode = 'RGB-RAW'


def is_right_green(raw):
	return raw[0] < 40 and raw[1] > 160 and raw[1] < 180 and raw[2] < 70

def is_left_green(raw):
	return raw[0] < 30 and raw[1] > 170 and raw[1] < 200 and raw[2] < 50

def is_right_blue(raw):
	return raw[0] < 50 and raw[1] > 120 and raw[1] < 150 and raw[2] < 150

def is_left_blue(raw):
	return raw[0] < 40 and raw[1] > 130 and raw[1] < 150 and raw[2] < 110

def is_right_red(raw):
	return raw[0] < 220 and raw[1] > 50 and raw[1] < 70 and raw[2] < 40

def is_left_red(raw):
	return raw[0] < 200 and raw[1] > 50 and raw[1] < 70 and raw[2] < 20

def is_right_yellow(raw):
	return raw[0] < 310 and raw[1] > 300 and raw[1] < 410 and raw[2] < 80

def is_left_yellow(raw):
	return raw[0] < 310 and raw[1] > 400 and raw[1] < 470 and raw[2] < 50



while(True):
	#print(ls.raw, rs.raw)
	llight = ls.raw
	rlight = rs.raw

	print(llight, rlight, is_main_trail(llight, rlight))

	# if is_left_green(llight) or is_right_green(rlight):
	# 	print("green")
	# 	sleep(1)
	# 	turn_back(tank)
		
	# elif is_left_red(llight) or is_right_red(rlight):
	# 	print("red")
	# 	sleep(1)
	# 	turn_90(1, tank)
	# elif is_left_yellow(llight) or is_right_yellow(rlight):
	# 	print("yellow")
	# 	sleep(1)
	# 	turn_90(-1, tank)
	# elif is_left_blue(llight) or is_right_blue(rlight):
	# 	print("blue")
	# else:
	# 	print("No color detected")

#  niebieski (24, 145, 103), (34, 134, 135)
#  czerwony  (189, 60, 11),  (209, 58, 28)
#  zielony   (22, 185, 33),  (35, 168, 56)
#  żółty     (284, 439, 36), (275, 353, 54)
#  szary	 (187, 375, 169), (203, 327, 209)
#  czarny    (11, 51, 8), (21, 44, 20)

