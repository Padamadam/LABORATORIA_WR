#!/usr/bin/env python3
import ev3dev.ev3 as ev3


class LineFollower():
    
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False
        
    
    def run(self):
        
        ls = ev3.ColorSensor(ev3.INPUT_4)
        rs = ev3.ColorSensor(ev3.INPUT_1)
        
        ls.mode = 'COLOR-REFLECT'
        ls.mode = 'COLOR-REFLECT'

        lm = ev3.LargeMotor('outA')
        rm = ev3.LargeMotor('outD')

        # lm.run_forever(time_sp=3000, speed_sp=500)
        # rm.run_timed(time_sp=3000, speed_sp=500)
        
        speed = 100
        
        Kp = 0.5
        dt = 0.01
        Ki = 0.5
        Kd = 0.5

        integral = 0
        previous_error = 0

        while not self.shut_down:
            lvalue = ls.reflected_light_intensity
            rvalue = rs.reflected_light_intensity
            
            error = lvalue - rvalue
            
            
            integral += (error*dt)
            derivative = (error-previous_error) / dt

            u = int((Kp*error) + (Ki*integral) + (Kd*derivative))

            print(u)

            if speed + u >= 500:
                lm.run_forever(speed_sp=500)
                rm.run_forever(speed_sp=-500)
            elif speed + u <= -500:
                lm.run_forever(speed_sp=-500)
                rm.run_forever(speed_sp=500)

            lm.run_forever(speed_sp=speed + u)
            rm.run_forever(speed_sp=speed - u)
            previous_error = error
            
            
if __name__ == "__main__":
    robot = LineFollower()
    robot.run()
