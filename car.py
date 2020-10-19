import time
from adafruit_motorkit import MotorKit

ACCELERATION = 0.5
MOVE_DURATION = 0.1

# MAX_SPEED prevents the motors from killing raspberry pi voltage
MAX_SPEED = 0.8


def limit_speed(speed):
    if speed > MAX_SPEED:
        speed = MAX_SPEED
    elif speed < -MAX_SPEED:
        speed = -MAX_SPEED

    return speed


class Car:
    def __init__(self, logger):
        self.logger = logger
        self.kit = MotorKit()
        self.motors = {
            "lf": self.kit.motor3,
            "rf": self.kit.motor4,
            "lr": self.kit.motor1,
            "rr": self.kit.motor2,
        }

        self.stop()

    def go(self, speed):
        self.speed = limit_speed(float(speed))
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
        self.move(MAX_SPEED, MAX_SPEED, MAX_SPEED, MAX_SPEED, MOVE_DURATION)

    def back(self):
        self.move(-MAX_SPEED, -MAX_SPEED, -MAX_SPEED, -MAX_SPEED, MOVE_DURATION)

    def left(self):
        self.move(-MAX_SPEED, MAX_SPEED, -MAX_SPEED, MAX_SPEED, MOVE_DURATION)

    def right(self):
        self.move(MAX_SPEED, -MAX_SPEED, MAX_SPEED, -MAX_SPEED, MOVE_DURATION)

    def move(self, lf, rf, lr, rr, duration):
        prev = self.get_throttle()
        self.set_throttle(lf, rf, lr, rr)
        time.sleep(duration)
        self.set_throttle(*prev)

    def get_throttle(self):
        return (
            self.motors["lf"].throttle,
            self.motors["rf"].throttle,
            self.motors["lr"].throttle,
            self.motors["rr"].throttle,
        )

    def set_throttle(self, lf, rf, lr, rr):
        for name, speed in [("lf", lf), ("rf", rf), ("lr", lr), ("rr", rr)]:
            self.motors[name].throttle = limit_speed(speed)
