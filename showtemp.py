#!/usr/bin/env python3

import os, re
import curses
from widgets import rectangle
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
        
        self.win.addstr(0,0,"Temperature:")
        self.label = Label(self.win, 1, 2, self.width-2, "-", padding_left=1).draw()
        rectangle(self.win,0,1,self.width,self.height-1)
    
    def show(self):
        sf = open("/sys/bus/w1/devices/"+self.sensor+"/w1_slave")
        if (re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", sf.readline())):
            temp = float(re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", sf.readline()).group(2))/1000
            self.label.update_text(str(temp)+" °C").draw()
        else:
            self.label.update_text("-").draw()
        self.win.refresh()

