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

left_straight = 10
right_straight = 10
turn_drop = 10
arm_speed = -100
gap_time = 5
eject_time = 10
arm_lift_time = 3

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
    last_command = None
    cargo_ejected = False
    while True:
        
        left_black = (left_sensor.value == 1)
        right_black = (right_sensor.value == 1)
        drop_off_detected = (hall_sensor.value == 1)
        now = time.monotonic()
        
        print("Left ", left_sensor.value, "Right ", right_sensor.value, "Hall ", hall_sensor.value)
        
        if left_black or right_black:
            white_since = None
        else:
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
            
        if start_time - now >= eject_time and not cargo_ejected:
            print(f"{eject_time} seconds passed. Ejecting cargo...")
            arm.start(arm_speed)
            time.sleep(arm_lift_time)
            cargo_ejected = True
        elif drop_off_detected and not cargo_ejected:
            print("Hall sensor magnetic field detected. Ejecting cargo...")
            arm.start(arm_speed)
            time.sleep(arm_lift_time)
            cargo_ejected = True
        
            
        
            
except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")
finally:
    # Always stop both motors
    stop()


