#!/usr/bin/env python3

import os, re

import curses
from curses.textpad import Textbox, rectangle
from datetime import datetime
from curses import wrapper

class tempwin:
    def __init__(self, xpos, ypos, width, height, sensor):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.sensor = sensor
    def show(self):
        self.win.erase()
        self.win.addstr(0, 0, "Temperature:")
        rectangle(self.win, 1,0, self.height-2,self.width-2)
        sf = open("/sys/bus/w1/devices/"+self.sensor+"/w1_slave")
        if (re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", sf.readline())):
            temp = float(re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", sf.readline()).group(2))/1000
            self.win.addstr(2,2, str(temp)+" °C")
        else:
            self.win.addstr(2,2, "-")
        self.win.refresh()

