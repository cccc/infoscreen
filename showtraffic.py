#!/usr/bin/env python3

import curses
from widgets import Table, rectangle, Label

class trafficwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        
        self.label = Label(self.win, 0, 0, self.width, "Traffic not connected").draw()
        self.table = Table(
                self.win,
                1,
                2,
                width-2,
                height-3,
                [
                    { # LINE
                        "width": 10,
                        "text": lambda col,row,dep,data: "   "+dep["line"],
                        "attributes": [curses.color_pair(0), curses.color_pair(3)]
                    },
                    { # DIRECTION
                        "width": width-8-9-6-5,
                        "text": lambda col,row,dep,data: dep["direction"],
                        "attributes": [curses.color_pair(0), curses.color_pair(3)]
                    },
                    { # PLATFORM
                        "width": 6,
                        "text": lambda col,row,dep,data: dep["platform"],
                        "attributes": [curses.color_pair(0), curses.color_pair(3)]
                    },
                    { # TIME
                        "width": 6,
                        "text": lambda col,row,dep,data: dep["departure"] if "departure" in dep else "",
                        "attributes": [curses.color_pair(0),curses.color_pair(3)]
                    },
                    { # DELAY
                        "width": 4,
                        "text": lambda col,row,dep,data: dep["delay"],
                        "attributes": [curses.color_pair(0), curses.color_pair(3)] 
                    },
                ],
                {
                    "line_delay": 0.025
                }
            )
        rectangle(self.win,0,1,self.width,self.height-1)

    def update(self, dep):
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLUE)

        try:
            #delays = sum(map(lambda x: x["delay"] if "delay" in x and x["delay"] > 0 else 0, dep["departures"]))
            #" | Total Delay: %d Min." % (delays) if delays > 0 else ""
            delays = 0
            
            self.label.update_text("Departures %s" % dep['srvtime']).draw()
            self.table.apply_data(dep["departures"])
                
        except Exception as msg:
            self.win.addstr(2,2,"Something went wrong! " + str(msg), curses.color_pair(1))

    def show(self):
        self.win.refresh()

