#!/usr/bin/env python3

import os
import time
import sys
import signal
import time
import curses

from car import Car


class Logger:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def log(self, str):
        self.stdscr.insertln()
        self.stdscr.addstr(0, 0, str)
        self.stdscr.refresh()


class Window:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(True)
        self.stdscr.clear()

        self.logger = Logger(self.stdscr)
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
                key = self.stdscr.getch()

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


curses.wrapper(lambda w: Window(w).main())