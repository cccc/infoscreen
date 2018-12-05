import curses
from widgets import Table, rectangle

class heartbeatwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        
        self.table = Table(
            self.win,
            2,
            2,
            self.width-3,
            self.height-3,
            [
                {
                    "width": self.width-3,
                    "text": lambda col, row, item, data: item[0],
                    "attributes": lambda col, row, item, data: curses.color_pair(2) if item[1] else curses.color_pair(1)
                }
            ])
        
        self.win.addstr(0, 0, 'Infrastructure:')
        rectangle(self.win,0,1,self.width,self.height-1)
        self.heartbeats = {}

    def update(self, topic, payload):
        if len(payload) == 0:
            self.heartbeats.pop(topic[len('heartbeat/'):])

        else:
            self.heartbeats[topic[len('heartbeat/'):]] = payload[0]
        
        self.table.apply_data( list(sorted(self.heartbeats.items())) )

    def show(self):
        self.win.refresh()
