#!/usr/bin/env python3

import curses

class weatherwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height, width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos

    def update(self, data):
        print("got message")
        self.window.addstr(0,0,data)

    def show(self):
        self.win.refresh()

 
