import math
from time import sleep

from pylgbst import get_connection_bleak
from pylgbst.hub import MoveHub
from pylgbst.peripherals import EncodedMotor

class ZetrosInterface:

    def __init__(self):
        self.current_angle = 0
        self.center = 0
        self.margin = 0
        self.time = 3

        self.hub = MoveHub(connection=get_connection_bleak(hub_name='Technic Hub'))
        self.hub.motor_external.subscribe(self.angle, mode=EncodedMotor.SENSOR_ANGLE)
        self.calibrate_angle()

    def angle(self, a):
        self.current_angle = a

    def calibrate_angle(self):
        self.hub.motor_external.timed(2, -0.6, wait_complete=True)
        sleep(1)
        left_angle = self.current_angle
        self.hub.motor_external.timed(2, 0.6, wait_complete=True)
        sleep(1)
        right_angle = self.current_angle
        self.center = (left_angle + right_angle) // 2
        self.margin = min((self.center - left_angle), (right_angle - self.center))
        self.hub.motor_external.goto_position(self.center, speed=0.6, wait_complete=True)

    def user_drive(self, where):
        if where == "left":
            self.hub.motor_external.goto_position(self.center - self.margin, wait_complete=True)
            self.hub.motor_A.timed(self.time, 1)
        elif where == "right":
            self.hub.motor_external.goto_position(self.center + self.margin, wait_complete=True)
            self.hub.motor_A.timed(self.time, 1)
        elif where == "forward":
            self.hub.motor_external.goto_position(self.center, wait_complete=True)
            self.hub.motor_A.timed(self.time, 1)
        elif where == "backward":
            self.hub.motor_external.goto_position(self.center, wait_complete=True)
            self.hub.motor_A.timed(self.time, -1)
        else:
            raise ValueError("Where must be 'left', 'right', or 'forward'")

