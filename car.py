import time
from adafruit_motorkit import MotorKit

ACCELERATION = 0.5
MOVE_DURATION = 0.1


class Car:
    def __init__(self, logger):
        self.logger = logger
        self.kit = MotorKit()
        self.stop()

    def go(self, speed):
        # sensible speed limit
        if speed > 1:
            speed = 1
        elif speed < -1:
            speed = -1

        self.speed = float(speed)
        self.set_throttle(self.speed, self.speed, self.speed, self.speed)

    def stop(self):
        self.go(0)

    def accelerate(self):
        if self.speed < 0:
            # if moving backwards, stop
            self.stop()
        else:
            # otherwise, forward
            self.go(self.speed + ACCELERATION)

    def decelerate(self):
        if self.speed > 0:
            # if moving forward, stop
            self.stop()
        else:
            # otherwise, reverse
            self.go(self.speed - ACCELERATION)

    def forward(self):
        self.move(1, 1, 1, 1, MOVE_DURATION)

    def back(self):
        self.move(-1, -1, -1, -1, MOVE_DURATION)

    def left(self):
        self.move(-1, 1, -1, 1, MOVE_DURATION)

    def right(self):
        self.move(1, -1, 1, -1, MOVE_DURATION)

    def move(self, lf, rf, lr, rr, duration):
        orig_lf = self.kit.motor1.throttle
        orig_rf = self.kit.motor2.throttle
        orig_lr = self.kit.motor3.throttle
        orig_rr = self.kit.motor4.throttle

        self.set_throttle(lf, rf, lr, rr)
        time.sleep(duration)
        self.set_throttle(orig_lf, orig_rf, orig_lr, orig_rr)

    def set_throttle(self, lf, rf, lr, rr):
        self.kit.motor1.throttle = lf
        self.kit.motor2.throttle = rf
        self.kit.motor3.throttle = lr
        self.kit.motor4.throttle = rr
