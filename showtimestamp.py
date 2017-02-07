#!/usr/bin/env python3

import curses
import time
from curses.textpad import Textbox, rectangle
from datetime import datetime
from curses import wrapper

class timewin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
    def show(self):
        self.win.erase()
        self.win.addstr(0, 0, "Current time:")
        rectangle(self.win, 1,0, self.height-2,self.width-2)
        self.win.addstr(2,2, "{:%H:%M:%S}".format(datetime.now()))
        self.win.refresh()

