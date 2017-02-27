#!/usr/bin/env python3
import curses
from curses.textpad import Textbox, rectangle
from datetime import datetime
from curses import wrapper

class mpdwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos

        self.state = None
        self.song = ''

    def update_state(self, state):
        self.state = state
        self.update()
    def update_song(self, song):
        self.song = song
        self.update()
    
    def update(self):
        self.win.erase()

        if self.state == 'pause':
            self.win.addstr(0,0, "Paused:")
        elif self.state == 'play':
            self.win.addstr(0,0, "Now Playing:")
        elif self.state == 'stop':
            self.win.addstr(0,0, "Stopped.")

        rectangle(self.win,1,0,self.height-2,self.width-1)

        self.win.addstr(2,2,self.song[0:self.width-3])

    def show(self):
        self.win.refresh()
