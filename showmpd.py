#!/usr/bin/env python3
from musicpd import (MPDClient, CommandError)
import curses
from curses.textpad import Textbox, rectangle
from datetime import datetime
from curses import wrapper

class mpdwin:
    def __init__(self, xpos, ypos, width, height, host):
        self.client = MPDClient()
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.host = host
    
    def show(self):
        self.win.erase()
        self.win.addstr(0,0, "Now Playing:")
        rectangle(self.win,1,0,self.height-2,self.width-1)
        try:
            self.client.connect(self.host, 6600)
            self.win.addstr(2,2,self.client.currentsong().get('file',0)[0:self.width-3])
            self.client.disconnect()
        except:
            self.win.addstr(2,2,"Something went wrong!", curses.color_pair(1));
        self.win.refresh()

