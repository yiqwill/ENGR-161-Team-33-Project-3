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
    
def stop_motors():
    left_drive.stop()
    right_drive.stop()
    arm.stop()
    
try:
    arm.start(arm_speed)
    time.sleep(arm_lift_time)
    arm.stop()
    while True:
        
        left_black = (left_sensor.value == 1)
        right_black = (right_sensor.value == 1)
        drop_off_detected = (hall_sensor.value == 1)
        
        print("Left ", left_sensor.value, "Right ", right_sensor.value, "Hall ", hall_sensor.value)
        
         
except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")
finally:
    # Always stop both motors
    stop_motors()


