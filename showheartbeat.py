import curses
from curses.textpad import Textbox, rectangle

class heartbeatwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos

        self.heartbeats = {}

    def update(self, topic, payload):
        self.heartbeats[topic[len('heartbeat/'):]] = payload[0]

        self.win.erase()
        rectangle(self.win,1,0,self.height-2,self.width-1)

        self.win.addstr(0, 0, 'Infrastructure:')

        for i, (s, v) in enumerate(sorted(self.heartbeats.items())[:23]):

            if v != 0:
                color = curses.color_pair(2)
            else:
                color = curses.color_pair(1)

            self.win.addstr(2 + i, 2, s, color)

    def show(self):
        self.win.refresh()
