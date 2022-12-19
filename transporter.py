#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time as tm

USE_BUTTON = False


class LineFollower():
    
    def __init__(self):
        pass
        
    
    def run(self):
        
        ls = ev3.ColorSensor(ev3.INPUT_4)
        rs = ev3.ColorSensor(ev3.INPUT_1)
        infra = ev3.InfraredSensor(ev3.INPUT3)

        if USE_BUTTON:
            btn = ev3.TouchSensor(ev3.INPUT_2)

        ls.mode = 'RGB-RAW'
        ls.mode = 'RGB-RAW'

        lm = ev3.LargeMotor('outD')
        rm = ev3.LargeMotor('outA')
        servo = ev3.MediumMotor('outB')

        # lm.run_forever(time_sp=3000, speed_sp=500)
        # rm.run_timed(time_sp=3000, speed_sp=500)
        
        speed = 200
        
        Kp = 2
        # dt = 0.01
        Ki = 0.0
        Kd = 0.0
	
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

            lvalue = sum(ls.raw)/3
            rvalue = sum(rs.raw)/3
            
            error = (lvalue - rvalue) / 5  # dostosowywanie rzedu wielkosci
            
            t_new = tm.perf_counter()
            dt = t_new - t_last
            t_last = t_new

            integral += (error*dt)
            derivative = (error-previous_error) / dt

            u = int((Kp*error) + (Ki*integral) + (Kd*derivative))

            print(dt)
            print("u:",u, "lv:", round(lvalue,2), "rv:", round(rvalue,2), "err:", round(Kp*error, 2), "i:", round(Ki*integral, 2), "d", round(Kd*derivative, 2))
            

            #if speed + u >= 500:
            #    lm.run_timed(time_sp = 1000, speed_sp=500)
            #    rm.run_timed(time_sp = 1000, speed_sp=-500)
            #elif speed - u >= 500
            #   lm.run_timed(time_sp = 1000, speed_sp=-500)
            #   rm.run_timed(time_sp = 1000, speed_sp=500)
            #else:
            lm.run_timed(time_sp = 1000, speed_sp=speed + u)
            rm.run_timed(time_sp = 1000, speed_sp=speed - u)
            previous_error = error

            

            
if __name__ == "__main__":
    robot = LineFollower()
    robot.run()
