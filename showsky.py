import curses
from curses.textpad import rectangle
from datetime import datetime

class skywin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos

    def entry_to_str(self, entry):
        #entry['ptime'] = datetime.fromtimestamp(entry['timestamp']).strftime('%b %d, %H:%M:%S')
        #if entry['type'] == 'iss':
        #    return 'ISS   {brightness_float: 1.1f}  {altitude_deg:2}°    -   {ptime}'.format(**entry)
        #else:
        #    return 'Ir{satellite_num}  {brightness_float: 1.1f}  {altitude_deg:2}°  {azimuth_deg:3}°  {ptime}'.format(**entry)

        entry['ptime'] = datetime.fromtimestamp(entry['timestamp']).strftime('%a %H:%M:%S')

        if entry['type'] == 'iss':
            return 'ISS   {brightness_float: 1.1f}  {ptime}'.format(**entry)
        else:
            return 'Ir{satellite_num}  {brightness_float: 1.1f}  {ptime}'.format(**entry)

    def update(self, sky_data):
        self.win.erase()
        rectangle(self.win,1,0,self.height-2,self.width-1)

        self.win.addstr(0, 0, "Sky Events:")
        for i, entry in enumerate(sky_data[:self.height-4]):
            self.win.addstr(2+i, 2, self.entry_to_str(entry))

    def show(self):
        self.win.refresh()
