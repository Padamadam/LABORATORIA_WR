#!/usr/bin/env python3
import ev3dev.ev3 as ev3


class LineFollower():
    
    def __init__(self):
        pass
        
    
    def run(self):
        
        ls = ev3.ColorSensor(ev3.INPUT_4)
        rs = ev3.ColorSensor(ev3.INPUT_1)
        
        btn = ev3.TouchSensor(ev3.INPUT_2)

        ls.mode = 'RGB-RAW'
        ls.mode = 'RGB-RAW'

        lm = ev3.LargeMotor('outD')
        rm = ev3.LargeMotor('outA')

        # lm.run_forever(time_sp=3000, speed_sp=500)
        # rm.run_timed(time_sp=3000, speed_sp=500)
        
        speed = 300
        
        Kp = 12
        dt = 0.01
        Ki = 0.5
        Kd = 0.05
	
        integral = 0
        previous_error = 0

        # lm.run_forever(speed_sp=0)
        # rm.run_forever(speed_sp=0)
        is_running = False

        print("Robot ready")

        prev_pressed = False

        while(True):
            pressed = btn.is_pressed
            if pressed and not prev_pressed:
                is_running = not is_running
            prev_pressed = pressed

            if not is_running:
                continue

            lvalue = sum(ls.raw)/3
            rvalue = sum(rs.raw)/3
            
            error = (lvalue - rvalue) / 5  # dostosowywanie rzedu wielkosci
            
            
            integral += (error*dt)
            derivative = (error-previous_error) / dt

            u = int((Kp*error) + (Ki*integral) + (Kd*derivative))

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
