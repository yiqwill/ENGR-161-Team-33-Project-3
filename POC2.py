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

left_straight = 20
right_straight = 20
turn_drop = 25
arm_speed = -100
gap_time = 5
eject_time = 10
arm_lift_time = 1

# positive values - go forward
def drive(left_speed, right_speed):
    left_drive.start(left_speed * LEFT_DIRECTION)
    right_drive.start(right_speed * RIGHT_DIRECTION)
    
def stop_motors():
    left_drive.stop()
    right_drive.stop()
    arm.stop()
    
try:
    start_time = time.monotonic()
    last_command = None
    cargo_ejected = False
    while True:
        
        left_black = (left_sensor.value == 1)
        right_black = (right_sensor.value == 1)
        drop_off_detected = (hall_sensor.value == 1)
        now = time.monotonic()
        
        print("Left ", left_sensor.value, "Right ", right_sensor.value, "Hall ", hall_sensor.value)
            

        if left_black and not right_black:
            command = (left_straight - turn_drop, right_straight)

        elif right_black and not left_black:
            command = (left_straight, right_straight - turn_drop)

        else:
            command = (left_straight, right_straight)

        if command != last_command:
            drive(*command)
            time.sleep(0.1)
            last_command = command
            print(f"Left black: {left_black}, Right black: {right_black}, "f"Command: {command}", f"Time {(now - start_time):.2f}")
            
        if not cargo_ejected and (now - start_time >= eject_time or drop_off_detected):
            print(f"Ejecting cargo... Hall Sensor? {drop_off_detected}")
            stop_motors()

            arm.start(arm_speed)
            time.sleep(arm_lift_time)
            arm.start(-arm_speed)
            time.sleep(arm_lift_time)
            arm.stop()

            cargo_ejected = True
            last_command = None
            white_since = None
        
         
except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")
finally:
    # Always stop both motors
    stop_motors()



