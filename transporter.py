#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import MediumMotor
from ev3dev2.sensor.lego import InfraredSensor
import time as tm

USE_BUTTON = True

def set_modules():
    if USE_BUTTON:
        btn = ev3.TouchSensor(ev3.INPUT_2)
    
    ls = ev3.ColorSensor(ev3.INPUT_4)
    rs = ev3.ColorSensor(ev3.INPUT_1)
    ls.mode = 'RGB-RAW'
    ls.mode = 'RGB-RAW'
    lm = ev3.LargeMotor('outD')
    rm = ev3.LargeMotor('outA')
    servo = MediumMotor('outB')
    infra = InfraredSensor(ev3.INPUT_3)
    return ls, rs, lm, rm, btn, infra, servo
    


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

def detected_color(llight, rlight):
    if is_left_green(llight):
        return "green", -1
    if is_right_green(rlight):
        return "green", 1
    if is_left_red(llight):
        return "red", -1
    if is_right_red(rlight):
        return "red", 1
    if is_left_yellow(llight):
        return "yellow", -1
    if is_right_yellow(rlight):
        return "yellow", 1
    if is_left_blue(llight):
        return "blue", -1
    if is_right_blue(rlight):
        return "blue", 1
    else:
        return None, 0

def regulator(llight, rlight, previous_error):
    
    Kp = 10
    dt = 0.01
    Ki = 1
    Kd = 0

    integral = 0

    lvalue = sum(llight)/3
    rvalue = sum(rlight)/3
    
    error = (lvalue - rvalue) / 5  # dostosowywanie rzedu wielkosci
    
    integral += (error*dt)
    derivative = (error-previous_error) / dt

    u = int((Kp*error) + (Ki*integral) + (Kd*derivative))

    print("u:",u, "lv:", round(lvalue,2), "rv:", round(rvalue,2), "err:", round(Kp*error, 2), "i:", round(Ki*integral, 2), "d", round(Kd*derivative, 2))

    return u, error

def get_packet(color, side, lm, rm):
    lm.run_timed(time_sp = 1000, speed_sp=0)
    rm.run_timed(time_sp = 1000, speed_sp=0)
    return

def run():
    
    ls, rs, lm, rm, btn, infra, servo = set_modules()
    speed = 150

    is_running = not USE_BUTTON

    print("Robot ready")

    prev_pressed = False

    previous_error = 0
    
    angle = 80

    servo.on_for_degrees(20, -angle)

    tm.sleep(5)

    servo.on_for_degrees(2, angle)

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
        if color is not None:
            get_packet(color, side, lm, rm)
        else:
            u, previous_error = regulator(llight, rlight, previous_error)
            lm.run_timed(time_sp = 1000, speed_sp=speed + u)
            rm.run_timed(time_sp = 1000, speed_sp=speed - u)


            
if __name__ == "__main__":
    run()
