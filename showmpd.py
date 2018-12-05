#!/usr/bin/env python3
import curses
from widgets import rectangle
from datetime import datetime
from curses import wrapper

class mpdwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height, width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos

        self.state = 'stop'
        self.song = ''
        
        rectangle(self.win,0,1,self.width,self.height-1)
        self.update()

    def update_state(self, state):
        self.state = state
        self.update()

    def update_song(self, song):
        self.song = song
        self.update()
    
    def update(self):
        #self.win.erase()

        if self.state == 'pause':
            self.win.addstr(0,0, "Paused:")
        elif self.state == 'play':
            self.win.addstr(0,0, "Now Playing:")
        elif self.state == 'stop':
            self.win.addstr(0,0, "Stopped.")


        self.win.addnstr(2,2,self.song, self.width-2)

    def show(self):
        self.win.refresh()
