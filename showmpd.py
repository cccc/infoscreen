#!/usr/bin/env python3
import curses
from widgets import rectangle, Label
from datetime import datetime
from curses import wrapper

class mpdwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height, width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        
        rectangle(self.win,0,1,self.width,self.height-1)
        self.state_label = Label(self.win, 0, 0, self.width, "MPD not Connected").draw()
        self.song_label = Label(self.win, 1, 2, self.width-2, padding_left=1)

    def update_state(self, state):
        if state == 'pause':
            self.state_label.update_text("Paused:").draw()
        elif state == 'play':
            self.state_label.update_text("Now Playing:").draw()
        elif state == 'stop':
            self.state_label.update_text("Stopped.").draw()

    def update_song(self, song):
        self.song_label.update_text(song).draw()

    def show(self):
        self.win.refresh()
