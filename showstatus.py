import curses
from curses import wrapper
from widgets import Label

class statuswin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        
        self.label = Label(self.win, 0, 0, self.width-1, "Status unknown", alignment=1).draw() #Needs -1 because python curses is stupid :(

    def update(self, payload):
        if payload[0] != 0:
            self.label.update_text("Club is open!").update_attributes(curses.color_pair(2)).draw()
        else:
            self.label.update_text("Club is closed!").update_attributes(curses.color_pair(1)).draw()

    def show(self):
        self.win.refresh()
