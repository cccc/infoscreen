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
        self.win.erase()
        rectangle(self.win,1,0,self.height-2,self.width-1)


    def update(self, dep):
        #self.win.erase()
        #rectangle(self.win,1,0,self.height-2,self.width-1)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLUE)

        try:
            #delays = sum(map(lambda x: x["delay"] if "delay" in x and x["delay"] > 0 else 0, dep["departures"]))
            delays = 0
            self.win.addstr(0,0,
                            "".join(("Departures ", dep['srvtime'],
                                     " | Total Delay: %d Min." % (delays) if delays > 0 else "")))
            #for s, nextdep in enumerate(dep['departures']):
            for s in range(0, self.height-4):
                #if (s > self.height-5):
                #    break
                self.win.addstr(2+s,2,' '*(self.width-3), curses.color_pair(0 if (s%2)==0 else 3))
                if (s < len(dep['departures'])):
                    nextdep = dep['departures'][s]
                    if ('timetable' in nextdep):
                        self.win.addstr(2+s, 2, nextdep['timetable'],curses.color_pair(0 if (s%2)==0 else 3))
                    self.win.addstr(2+s,10,(nextdep['line']+'\t'+nextdep['direction'])[0:self.width-31], curses.color_pair(0 if (s%2)==0 else 3))
                    if (type(nextdep['reldeparture']) == int or type(nextdep['reldeparture']) == float):
                        self.win.addstr(2+s,self.width-20,("%d Min." % nextdep['reldeparture'] if nextdep['reldeparture'] >= 1 else "Sofort"),curses.color_pair(0 if (s%2)==0 else 3))
                    else:
                        self.win.addstr(2+s,self.width-20,str(nextdep['reldeparture']),curses.color_pair(0 if (s%2)==0 else 3))
                    if ('delay' in nextdep):
                        if (nextdep['delay'] > 1):
                            self.win.addstr(2+s,self.width-10,"(+%d Min)" % nextdep['delay'],curses.color_pair(1 if (s%2)==0 else 4))
                        elif (nextdep['delay'] < -1):
                            self.win.addstr(2+s,self.width-10,"(%d Min)" % nextdep['delay'],curses.color_pair(0 if (s%2)==0 else 3))
                        else:
                            self.win.addstr(2+s,self.width-10,"(+0 Min)",curses.color_pair(2 if (s%2)==0 else 5))
                self.win.refresh()
                time.sleep(0.05)
        except Exception as msg:
            self.win.addstr(2,2,"Something went wrong! " + str(msg), curses.color_pair(1))

    def show(self):
        self.win.refresh()

