from basehat import LineFinder
from buildhat import Motor
import time


LEFT_LINE_SENSOR_PORT = 16
RIGHT_LINE_SENSOR_PORT = 26
CARGO_MOTOR_PORT = 'A'
STEER_MOTOR_PORT = 'B'
DRIVE_MOTOR_PORT = 'D'

BASE_SPEED = 20
CHECK_INTERVAL = 0.5

MAX_LEFT = -30
MAX_RIGHT = 30

leftSensor = LineFinder(LEFT_LINE_SENSOR_PORT)
rightSensor = LineFinder(RIGHT_LINE_SENSOR_PORT)
cargoMotor = Motor(CARGO_MOTOR_PORT)
driveMotor = Motor(DRIVE_MOTOR_PORT)
steerMotor = Motor(STEER_MOTOR_PORT)

def turn_right():
    steerMotor.start(-20)

def turn_left():
    steerMotor.start(20)

try:
    CENTER = steerMotor.get_position()
    driveMotor.start(BASE_SPEED)
    while True:
        left = leftSensor.value
        right = rightSensor.value
        position = steerMotor.get_position() - CENTER
        print(f"Left: {left} Right: {right}")
        print(f"Steering motor position {position}")
        if left:
            turn_left()
            time.sleep(0.5)
            turn_right()
            
        elif right:
            turn_right()
        else:
            steerMotor.stop()

        time.sleep(1)

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")

finally:
    driveMotor.stop()
    steerMotor.stop()

