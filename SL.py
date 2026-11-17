from basehat import LineFinder
from buildhat import Motor
import time


LEFT_LINE_SENSOR_PORT = 16
RIGHT_LINE_SENSOR_PORT = 26
CARGO_MOTOR_PORT = 'A'
STEER_MOTOR_PORT = 'B'
DRIVE_MOTOR_PORT = 'D'

BASE_SPEED = 30

leftSensor = LineFinder(LEFT_LINE_SENSOR_PORT)
rightSensor = LineFinder(RIGHT_LINE_SENSOR_PORT)
cargoMotor = Motor(CARGO_MOTOR_PORT)
driveMotor = Motor(DRIVE_MOTOR_PORT)
steerMotor = Motor(STEER_MOTOR_PORT)

try:
    driveMotor.start(BASE_SPEED)

except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt:
    print("You pressed ctrl+C. Program terminating.")

finally:
    driveMotor.stop()
    steerMotor.stop()

