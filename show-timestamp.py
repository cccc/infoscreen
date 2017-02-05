#!/usr/bin/env python3

import time

import curses
from curses.textpad import Textbox, rectangle
from datetime import datetime


def main(stdscr):
    stdscr.addstr(0, 0, "Current time:")

    editwin = curses.newwin(5,30, 2,1)
    rectangle(stdscr, 1,0, 3, 11)

    while True:
        stdscr.addstr(2,2, "{:%H:%M:%S}".format(datetime.now()))
        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    main(stdscr)
