from buildhat import Motor
from basehat import LineFinder

import time

#CONFIRMED
right_drive = Motor('A')
left_drive = Motor('B')
arm = Motor('D')

left_sensor = LineFinder(24)
right_sensor = LineFinder(22)

LEFT_DIRECTION = -1
RIGHT_DIRECTION = 1

STRAIGHT_ADJ = 1.25

# positive values - go forward
def drive(left_speed, right_speed):
    left_drive.start(left_speed * LEFT_DIRECTION)
    right_drive.start(right_speed * RIGHT_DIRECTION)
    
try:
    start_time = time.monotonic()
    white_since = None
    while True:
        left_black = left_sensor.value == 1
        right_black = right_sensor.value == 1 
        print("Left ", left_sensor.value, "Right ", right_sensor.value)
        drive(20, 20)
        
        if left_black and right_black:
            drive(30, 30)
        elif left_black:
            drive(-15, 30)
        elif right_black:
            drive(30, -15)
        else:
            if white_since == None:
                white_since = time.monotonic()
        
        current_time = time.monotonic()
        # stop while arm is unloading
        if current_time - start_time >= 5:
            arm.start(30)
            time.sleep(3)
            arm.stop()

except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")
finally:
    # Always stop both motors
    left_drive.stop()
    right_drive.stop()


