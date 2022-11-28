#!/usr/bin/env python3
import ev3dev.ev3 as ev3

lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')

ls = ev3.ColorSensor(ev3.INPUT_4)
rs = ev3.ColorSensor(ev3.INPUT_1)

ls.mode = "RGB-RAW"
rs.mode = "RGB-RAW"

lm.run_timed(time_sp=3000, speed_sp=500)
rm.run_timed(time_sp=3000, speed_sp=500)

# while True:
#    ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])

Kp = 0.5
dt = 500
Ki = 0.5
Kd = 0.5
v = 100

integral = 0
derivative = 0
previous_error = 0

while True:
    lvalue = max(ls.raw)
    rvalue = max(rs.raw)
    error = lvalue - rvalue
    integral += error*dt
    derivative += error-previous_error / dt

    u = int((Kp*error) + (Ki*integral) + (Kd*derivative))
    u = min(max(u, 0), v)

    print(u)

    if u > 0:
        lm.run_timed(time_sp=dt, speed_sp=v-u)
        rm.run_timed(time_sp=dt, speed_sp=v+u)
    else:
        lm.run_timed(time_sp=dt, speed_sp=v+u)
        rm.run_timed(time_sp=dt, speed_sp=v-u)

        previous_error = error
