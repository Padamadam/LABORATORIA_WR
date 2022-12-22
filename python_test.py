#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor, TouchSensor
USE_BUTTON = True


"""
Uruchomienie modulow
"""
def set_modules():
    if USE_BUTTON:
        btn = TouchSensor(ev3.INPUT_2)
    
    ls = ColorSensor(ev3.INPUT_4)
    rs = ColorSensor(ev3.INPUT_1)
    ls.mode = 'COL-REFLECT'
    ls.mode = 'COL-REFLECT'
    lm = LargeMotor('outD')
    rm = LargeMotor('outA')
    return ls, rs, lm, rm, btn
    

"""
Regulator PID
"""
def regulator(lvalue, rvalue, previous_error):
    
    Kp = 5
    dt = 0.01
    Ki = 2
    Kd = 0.1

    integral = 0
    
    error = (lvalue - rvalue)
    integral += (error*dt)
    derivative = (error-previous_error) / dt

    u = int(Kp*(error + (Ki*integral) + (Kd*derivative)))

    print("u:",u, "lv:", round(lvalue,2), "rv:", round(rvalue,2), "err:", round(Kp*error, 2), "i:", round(Ki*integral, 2), "d", round(Kd*derivative, 2))

    return u, error


def run():        
    is_running = False
    prev_pressed = False
    
    speed = 300
    previous_error = 0
    ls, rs, lm, rm, btn = set_modules()
    
    print("Robot ready")

    while(True):
        if USE_BUTTON:
            pressed = btn.is_pressed
            if pressed and not prev_pressed:
                is_running = not is_running
            prev_pressed = pressed

            if not is_running:
                continue

        lvalue = ls.reflected_light_intensity
        rvalue = rs.reflected_light_intensity
        
        u, previous_error = regulator(lvalue, rvalue, previous_error)

        if speed + u >= 1000:
            lm.run_timed(time_sp = 1000, speed_sp=1000)
            rm.run_timed(time_sp = 1000, speed_sp=-1000)
        elif speed - u >= 1000:
            lm.run_timed(time_sp = 1000, speed_sp=-1000)
            rm.run_timed(time_sp = 1000, speed_sp=1000)
        else:
            lm.run_timed(time_sp = 1000, speed_sp=speed + u)
            rm.run_timed(time_sp = 1000, speed_sp=speed - u)

            
if __name__ == "__main__":
    run()
