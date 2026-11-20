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
    
    time.sleep(10)
    
except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")
finally:
    # Always stop both motors
    left_drive.stop()
    right_drive.stop()

