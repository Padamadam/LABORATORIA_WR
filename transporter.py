#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import MediumMotor, LargeMotor, MoveTank
from ev3dev2.sensor.lego import InfraredSensor, ColorSensor, TouchSensor
import time as tm

"""
UWAGI:
- poprawilem algorytm PID: stala Kp wymnaza wszystkie czlony w rownaniu
- infrared byc moze bedzie lepiej uzywac funkcji value niz proximity
- przy dojezdzie do koszyka obliczylbym czas dojazdu, nie stosowalbym juz line followingu
- trzeba zobaczyc jak zachowuje sie robot przy napotkaniu koloru na czarnej linii: mozliwe ze skreca
- sledznie linii przenioslbym do odzielnej funkcji, poniewaz moze uzyje sie go w dwoch miejscach

"""

USE_BUTTON = True

"""
Uruchomienie modulow
"""
def set_modules():
    if USE_BUTTON:
        btn = TouchSensor(ev3.INPUT_2)
    else:
        btn = None
    
    ls = ColorSensor(ev3.INPUT_4)
    rs = ev3.ColorSensor(ev3.INPUT_1)
    ls.mode = 'RGB-RAW'
    ls.mode = 'RGB-RAW'
    lm = LargeMotor('outD')
    rm = LargeMotor('outA')
    servo = MediumMotor('outC')
    infra = InfraredSensor(ev3.INPUT_3)
    tank =  MoveTank('outD', 'outA')
    return ls, rs, lm, rm, btn, infra, servo, tank
    

"""
Wykrywanie kolorow
funkcje boolowskie, zwracaja czy kolor zostal wykryty
Funkcja detected_color zwarca nazwe koloru oraz strone z ktorej zostal wykryty
-1: lewy
1: prawy
"""
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

def is_left_black(raw):
    return raw[0] < 20 and raw[1] < 60 and raw[2] < 20

def is_right_black(raw):
    return raw[0] < 30 and raw[1] < 55 and raw[2] < 30

def is_main_trail(llight, rlight):
    left_black = is_left_black(llight)
    right_black = is_right_black(rlight)
    left_yellow = is_left_yellow(llight)
    right_yellow = is_right_black(rlight)

    if left_yellow and right_yellow:
        return False
    return (left_black or left_yellow) and (right_black or right_yellow)

def are_green(llight, rlight):
    return is_left_green(llight) and is_right_green(rlight)

def detected_color(llight, rlight):
    if is_left_green(llight):
        return "green", -1
    if is_right_green(rlight):
        return "green", 1
    # if is_left_red(llight):
    #     return "red", -1
    # if is_right_red(rlight):
    #     return "red", 1
    if is_left_yellow(llight):
        return "yellow", -1
    if is_right_yellow(rlight):
        return "yellow", 1
    # if is_left_blue(llight):
    #     return "blue", -1
    # if is_right_blue(rlight):
    #     return "blue", 1
    else:
        return None, 0

def regulator(llight, rlight, previous_error):
    
    # Kp = 10
    Kp = 7
    dt = 0.01
    Ki = 1
    Kd = 0

    integral = 0

    # obliczanie sredniej wartosci wykrytych danych RGB
    lvalue = sum(llight)/3
    rvalue = sum(rlight)/3
    
    error = (lvalue - rvalue) / 5  # dostosowywanie rzedu wielkosci
    integral += (error*dt)
    derivative = (error-previous_error) / dt

    u = int(Kp*error + Ki*integral + Kd*derivative)

    print("u:",u, "lv:", round(lvalue,2), "rv:", round(rvalue,2), "err:", round(Kp*error, 2), "i:", round(Ki*integral, 2), "d", round(Kd*derivative, 2))

    return u, error


def turn_back(tank):    # zawrocenie o 180 stopni
    tank.on_for_degrees(-10, 10, 160*3)
    
def turn_90(side, tank, ls, rs, lm, rm): # skret o 90 stopni

    if side == -1:

        while not is_right_yellow(rs.raw):
            lm.run_timed(time_sp = 1000, speed_sp=-150)
            rm.run_timed(time_sp = 1000, speed_sp=150)
    elif side == 1:
        while not is_left_yellow(ls.raw):
            lm.run_timed(time_sp = 1000, speed_sp=150)
            rm.run_timed(time_sp = 1000, speed_sp=-150)

        #tank.on_for_degrees(10, -10, 80*3)  
         
def approach(side, tank, infra, ls, rs, lm, rm):
    # lm.run_timed(time_sp = 1000, speed_sp=0)
    # rm.run_timed(time_sp = 1000, speed_sp=0)
    speed = 150
    previous_error = 0

    tank.on_for_seconds(10, 10, 1)
    turn_90(side, tank, ls, rs, lm, rm)
    while(infra.value() > 5):
        # tank.on(10, 10)
        u, previous_error = regulator(ls.raw, rs.raw, previous_error)
        lm.run_timed(time_sp = 1000, speed_sp=speed + u)
        rm.run_timed(time_sp = 1000, speed_sp=speed - u)
    tank.off()


def lift(servo):
    angle = 80
    servo.on_for_degrees(20, -angle)
    
    # testowe opuszczanie
    # tm.sleep(5)
    # servo.on_for_degrees(2, angle)

def put_down(servo):
    angle = 80
    servo.on_for_degrees(2, angle)
    
    
def reach_dropoff(lm, rm, ls, rs):
    speed = 10
    previous_error = 0
    llight = ls.raw
    rlight = rs.raw

    u, previous_error = regulator(llight, rlight, previous_error)
    lm.run_timed(time_sp = 1000, speed_sp=speed + u)
    rm.run_timed(time_sp = 1000, speed_sp=speed - u)

    
def get_package(side, tank, infra, servo, lm, rm, ls, rs):
    approach(side, tank, infra, ls, rs, lm, rm)
    lift(servo)
    turn_back(tank)
    previous_error = 0
    speed = 150
    llight, rlight = ls.raw, rs.raw
    while not is_main_trail(llight, rlight):
        u, previous_error = regulator(llight, rlight, previous_error)
        lm.run_timed(time_sp = 1000, speed_sp=speed + u)
        rm.run_timed(time_sp = 1000, speed_sp=speed - u)
        llight, rlight = ls.raw, rs.raw
    tank.on_for_seconds(10, 10, seconds=1)
    turn_90(-side, tank)


def put_package(side, tank, infra, servo, lm, rm, ls, rs):
    angle = 80
    speed = 150
    previous_error = 0
    tank.on_for_seconds(10, 10, 1)
    turn_90(side, tank)
    llight, rlight = ls.raw, rs.raw
    while not are_green(llight, rlight):
        u, previous_error = regulator(llight, rlight, previous_error)
        lm.run_timed(time_sp = 1000, speed_sp=speed + u)
        rm.run_timed(time_sp = 1000, speed_sp=speed - u)
        llight, rlight = ls.raw, rs.raw

    put_down(servo)
    tank.on_for_seconds(-10, -10, seconds=3)


def run():
    is_running = not USE_BUTTON
    prev_pressed = False

    ls, rs, lm, rm, btn, infra, servo, tank = set_modules()
    speed = 150

    
    print("Robot ready")

    state_get = True

    previous_error = 0
    
    while(True):
        if USE_BUTTON:
            pressed = btn.is_pressed
            if pressed and not prev_pressed:
                is_running = not is_running
            prev_pressed = pressed

        if not is_running:
            continue

        llight = ls.raw
        rlight = rs.raw

        print(infra.proximity)
        color, side = detected_color(llight, rlight)
        print("color", color, llight, rlight)
        if color == "yellow" and state_get:
            get_package(side, tank, infra, servo, lm, rm, ls, rs)
            state_get = False
        elif color == "green" and not state_get:
            put_package(side, tank, infra, servo, lm, rm, ls, rs)
            break
        else:
            u, previous_error = regulator(llight, rlight, previous_error)
            lm.run_timed(time_sp = 1000, speed_sp=speed + u)
            rm.run_timed(time_sp = 1000, speed_sp=speed - u)


            
if __name__ == "__main__":
    run()
