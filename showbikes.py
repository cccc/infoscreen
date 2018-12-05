#!/usr/bin/env python3

import curses
from datetime import datetime
from curses import wrapper
from widgets import Table, rectangle

class bikeswin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height, width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.table = Table(self.win,1,2,width-2,height-3,[{
                "text": lambda col,row,bike,data: ("#%s" % bike["bike_number"]) if "bike_number" in bike else "",
                "attributes":[curses.color_pair(0),curses.color_pair(3)],
                "width": 8
            },{
                "text": lambda col,row,bike,data: str(bike["address"] or "") if "address" in bike else "",
                "attributes":[curses.color_pair(0),curses.color_pair(3)],
                "width":width-2-8-5
            },{
                "text": lambda col,row,bike,data: ("%dm" % bike["distance"]) if "distance" in bike else "",
                "attributes":[curses.color_pair(0),curses.color_pair(3)],
                "width":5
            }],
            {
                "line_delay": 0.025
            })
        self.win.erase()
        rectangle(self.win,0,1,self.width,self.height-1)

    def update(self, data):
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        
        try:
            self.win.addstr(0,0,"Bikes %s" % data['time'])
            
            bikes = data["bikes"]
            bikes.sort(key=lambda bike: bike["distance"])
            self.table.apply_data(bikes)
        except Exception as msg:
            self.win.addstr(2,2,"Something went wrong! " + str(msg), curses.color_pair(1))

    def show(self):
        self.win.refresh()

