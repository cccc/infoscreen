#!/usr/bin/env python3

import time

import curses
from curses.textpad import Textbox, rectangle
from datetime import datetime
from curses import wrapper

class trafficwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos

    def update(self, dep):
        self.win.erase()
        rectangle(self.win,1,0,self.height-2,self.width-1)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLUE)

        try:
            self.win.addstr(0,0, "Departures "+dep['srvtime'])
            for nextdep in dep['departures']:
                self.win.addstr(2+s,2,' '*(self.width-3), curses.color_pair(0 if (s%2)==0 else 3))
                self.win.addstr(2+s,2,(nextdep['line']+'\t'+nextdep['direction'])[0:self.width-21], curses.color_pair(0 if (s%2)==0 else 3))
                self.win.addstr(2+s,self.width-20,("%d Min." % nextdep['reldeparture'] if nextdep['reldeparture'] >= 1 else "Sofort"),curses.color_pair(0 if (s%2)==0 else 3))
                if ('delay' in nextdep):
                    if (nextdep['delay'] > 1):
                        self.win.addstr(2+s,self.width-10,"(+%d Min)" % nextdep['delay'],curses.color_pair(1 if (s%2)==0 else 4))
                    else:
                        self.win.addstr(2+s,self.width-10,"(+0 Min)",curses.color_pair(2 if (s%2)==0 else 5))
        except:
            self.win.addstr(2,2,"Something went wrong!", curses.color_pair(1))
        self.win.refresh()

    def show()
        self.win.refresh()

