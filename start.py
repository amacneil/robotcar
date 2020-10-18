#!/usr/bin/env python3

import signal
import curses

from car import Car
from logger import Logger


class App:
    def __init__(self, window):
        self.window = window
        self.window.nodelay(True)
        self.window.clear()

        self.logger = Logger(self.window)
        self.car = Car(self.logger)
        self.done = False

        # handle ctrl-c
        signal.signal(signal.SIGINT, self.cleanup)

    def cleanup(self, signum, frame):
        self.done = True

    def main(self):
        while not self.done:
            # process recent keystrokes, find the most recent direction request
            # we do this to avoid a backlog of keystrokes if you hold down a key
            key = None
            direction = None
            while key != -1:
                if key == curses.KEY_UP:
                    direction = "forward"
                elif key == curses.KEY_DOWN:
                    direction = "back"
                elif key == curses.KEY_LEFT:
                    direction = "left"
                elif key == curses.KEY_RIGHT:
                    direction = "right"
                key = self.window.getch()

            # take action
            if direction == "forward":
                self.logger.log("Forward")
                self.car.accelerate()
            elif direction == "back":
                self.logger.log("Back")
                self.car.decelerate()
            elif direction == "left":
                self.logger.log("Left")
                self.car.left()
            elif direction == "right":
                self.logger.log("Right")
                self.car.right()

        self.car.stop()


curses.wrapper(lambda w: App(w).main())
