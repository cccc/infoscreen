#!/usr/bin/env python3

import time

import curses
from datetime import datetime
from curses import wrapper
from widgets import Table, rectangle
import numbers

class trafficwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.table = Table(
                self.win,
                1,
                2,
                width-2,
                height-3,
                [
                    { # TIME
                        "width": 8,
                        "text": lambda col,row,dep,data: dep["timetable"] if "timetable" in dep else "",
                        "attributes": [curses.color_pair(0),curses.color_pair(3)]
                    },
                    { # LINE
                        "width": 6,
                        "text": lambda col,row,dep,data: dep["line"] if "line" in dep else "",
                        "attributes": [curses.color_pair(0),curses.color_pair(3)]
                    },
                    { # DIRECTION
                        "width": self.width - 2 - 8 - 6 - 9 - 9,
                        "text": lambda col,row,dep,data: dep["direction"] if "direction" in dep else "",
                        "attributes": [curses.color_pair(0),curses.color_pair(3)]
                    },
                    { # RELTIME
                        "width": 9,
                        "text": lambda col,row,dep,data:
                            ("%d Min." % dep['reldeparture']) if isinstance(dep['reldeparture'], numbers.Number) else str(dep['reldeparture']),
                        "attributes": [curses.color_pair(0),curses.color_pair(3)]
                    },
                    { # DELAY
                        "width": 9,
                        "text": lambda col,row,dep,data:
                            ("(%+d Min)" % dep["delay"] ) if "delay" in dep else "",
                        "attributes": lambda col,row,dep,data:
                            curses.color_pair(
                                (1 if row%2 is 0 else 4) 
                                if dep["delay"] > 1 else
                                (
                                    (0 if row%2 is 0 else 3)
                                    if dep["delay"] < -1 else
                                    (2 if row%2 is 0 else 5)
                                )
                            )
                            if "delay" in dep else
                            curses.color_pair(0 if row%2 is 0 else 3),
                    }
                ],
                {
                    "line_delay": 0.025
                }
            )
        
        self.win.addstr(0,0,"Departures")
        rectangle(self.win,0,1,self.width,self.height-1)

    def update(self, dep):
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLUE)

        try:
            #delays = sum(map(lambda x: x["delay"] if "delay" in x and x["delay"] > 0 else 0, dep["departures"]))
            delays = 0
            self.win.addstr(0,0,"Departures %s" % dep['srvtime'])
            #" | Total Delay: %d Min." % (delays) if delays > 0 else ""
            
            self.table.apply_data(dep["departures"])
                
        except Exception as msg:
            self.win.addstr(2,2,"Something went wrong! " + str(msg), curses.color_pair(1))

    def show(self):
        self.win.refresh()

