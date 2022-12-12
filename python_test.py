#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time as tm

USE_BUTTON = True

# def bound(value, threshold):
#     return max(min(value, threshold), -threshold)

class LineFollower():
    
    def __init__(self):
        pass
        
    
    def run(self):
        
        ls = ev3.ColorSensor(ev3.INPUT_4)
        rs = ev3.ColorSensor(ev3.INPUT_1)
        
        if USE_BUTTON:
            btn = ev3.TouchSensor(ev3.INPUT_2)

        ls.mode = 'COL-REFLECT'
        ls.mode = 'COL-REFLECT'

        lm = ev3.LargeMotor('outD')
        rm = ev3.LargeMotor('outA')

        # lm.run_forever(time_sp=3000, speed_sp=500)
        # rm.run_timed(time_sp=3000, speed_sp=500)
        
        speed = 300
        
        Kp = 5
        dt = 0.01
        Ki = 2
        Kd = 0.1
	
        integral = 0
        previous_error = 0

        # lm.run_forever(speed_sp=0)
        # rm.run_forever(speed_sp=0)
        is_running = False

        print("Robot ready")

        prev_pressed = False
        t_last = tm.perf_counter()

        while(True):
            if USE_BUTTON:
                pressed = btn.is_pressed
                if pressed and not prev_pressed:
                    is_running = not is_running
                    t_last = tm.perf_counter()
                prev_pressed = pressed

                if not is_running:
                    continue

            lvalue = ls.reflected_light_intensity
            rvalue = rs.reflected_light_intensity
            
            error = (lvalue - rvalue)
            
            t_new = tm.perf_counter()
            dt_temp = t_new - t_last
            t_last = t_new

            integral += (error*dt)
            derivative = (error-previous_error) / dt

            u = int((Kp*error) + (Ki*integral) + (Kd*derivative))

            print(dt_temp)
            print("u:",u, "lv:", round(lvalue,2), "rv:", round(rvalue,2), "err:", round(Kp*error, 2), "i:", round(Ki*integral, 2), "d", round(Kd*derivative, 2))
            

            if speed + u >= 1000:
               lm.run_timed(time_sp = 1000, speed_sp=1000)
               rm.run_timed(time_sp = 1000, speed_sp=-1000)
            elif speed - u >= 1000:
              lm.run_timed(time_sp = 1000, speed_sp=-1000)
              rm.run_timed(time_sp = 1000, speed_sp=1000)
            else:
                lm.run_timed(time_sp = 1000, speed_sp=speed + u)
                rm.run_timed(time_sp = 1000, speed_sp=speed - u)
            previous_error = error

            
if __name__ == "__main__":
    robot = LineFollower()
    robot.run()
