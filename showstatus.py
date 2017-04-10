import curses
from curses import wrapper

class statuswin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos

        self.is_open = None

    def update(self, payload):
        self.is_open = payload[0] != 0

        self.win.erase()

        if (self.is_open):
            self.win.addstr(0,0, "Club is open!", curses.color_pair(2))
        else:
            self.win.addstr(0,0, "Club is closed!", curses.color_pair(1))

    def show(self):
        self.win.refresh()
