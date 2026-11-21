from buildhat import Motor
from basehat import LineFinder
from basehat import HallSensor
import time

#CONFIRMED
right_drive = Motor('A')
left_drive = Motor('B')
arm = Motor('D')

left_sensor = LineFinder(24)
right_sensor = LineFinder(22)
hall_sensor = HallSensor(26)

LEFT_DIRECTION = -1
RIGHT_DIRECTION = 1

STRAIGHT_ADJ = 1.25
left_straight = 10
right_straight = 10
turn_drop = 10
gap_time = 5

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
        drop_off_detected = (hall_sensor.value == 1)
        
        print("Left ", left_sensor.value, "Right ", right_sensor.value, "Hall ", hall_sensor.value)
        
        if left_black or right_black:
            white_since = None
        else:
            now = time.monotonic()
            
            if white_since is None:
                white_since = now
            
            if now - white_since >= gap_time:
                break #lost the line
            
        if left_black == right_black:
            command = (left_straight, right_straight)
        elif left_black:
            command = (left_straight - turn_drop, right_straight)
        else:
            command = (left_straight, right_straight - turn_drop)

        if command != last_command:
            drive(*command)
            last_command = command
            
except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")
finally:
    # Always stop both motors
    stop()


