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
left_straight = 10
right_straight = 10
turn_drop = 10

# positive values - go forward
def drive(left_speed, right_speed):
    left_drive.start(left_speed * LEFT_DIRECTION)
    right_drive.start(right_speed * RIGHT_DIRECTION)
    
def stop():
    left_drive.stop()
    right_drive.stop()
    arm.stop()
    
try:
    start_time = time.monotonic()
    white_since = None
    while True:
        left_black = (left_sensor.value == 1)
        right_black = (right_sensor.value == 1)
        print("Left ", left_sensor.value, "Right ", right_sensor.value)
        drive(20, 20)
        
        if left_black and right_black:
            drive(left_straight, right_straight)
        elif left_black:
            drive(left_straight - turn_drop, right_straight)
        elif right_black:
            drive(left_straight, right_straight - turn_drop)
        else:
            white_since = time.monotonic()
            current_time = time.monotonic()
            if time.monotonic() - white_since >= 3:
                print("White detected for 3 seconds. Stopping.")
                stop()
        # stop while arm is unloading
            elif current_time - start_time >= 5:
                arm.start(30)
                time.sleep(3)
                arm.stop()

except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")
finally:
    # Always stop both motors
    stop()


