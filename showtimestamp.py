#!/usr/bin/env python3

import curses
import time
from datetime import datetime
from curses import wrapper
from widgets import rectangle

class timewin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.win.addstr(0, 0, "Current time:")
        rectangle(self.win, 0, 1, self.width, self.height-1)
        
    def show(self):
        self.win.addstr(2,2, "{:%H:%M:%S}".format(datetime.now()))
        self.win.refresh()

