#!/usr/bin/env python3

import os
import curses

import showtimestamp
import showmpd
import showtraffic
import showtemp
import showstatus
import showheartbeat
import showsky

from infoscreen import Infoscreen


class Livingroom(Infoscreen):

    mpd_name = 'baellebad'

    def _init_windows(self):

        self.statusw = showstatus.statuswin(40,2,20,1)
        self.trafficw = showtraffic.trafficwin(1,11,76,23)
        self.tempw = showtemp.tempwin(20, 1, 14, 5, "28-000008a0fd0b")
        self.timew = showtimestamp.timewin(1,1,13,5)
        self.mpdw = showmpd.mpdwin(1,6,76,5)
        self.hbw = showheartbeat.heartbeatwin(79,11,28,23)
        self.skyw = showsky.skywin(79,1,28,10)


def main(stdscr):
            
    os.system("setterm --blank poke")
    os.system("setterm --blank 0")

    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    info_screen = Livingroom("infoscreen/livingroom", stdscr)
    info_screen.run()

if __name__ == "__main__":
    curses.wrapper(main)
