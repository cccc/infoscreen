import curses
from datetime import datetime
from widgets import Table, rectangle

class skywin:
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
            self.width-2,
            self.height-3,
            [
                { #TYPE
                    "width": 6,
                    "text": lambda col, row, entry, data: "ISS" if entry['type'] == "iss" else "Ir%2d" % entry["satellite_num"]
                },
                { #BRIGHTNESS
                    "width": self.width - 2 - 6 - 12,
                    "text": lambda col, row, entry, data: "%1.1f" % entry["brightness_float"]
                },
                { #TIME
                    "width": 12,
                    "text": lambda col, row, entry, data: datetime.fromtimestamp(entry['timestamp']).strftime('%a %H:%M:%S')
                }
            ])
        
        self.win.addstr(0, 0, "Sky Events:")
        rectangle(self.win,0,1,self.width,self.height-1)

    def update(self, sky_data):
        try:
            self.table.apply_data(sky_data)
        except Exception as msg:
            self.win.addstr(2, 1, msg)

    def show(self):
        self.win.refresh()
