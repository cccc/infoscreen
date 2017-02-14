#!/usr/bin/env python3

import time

import os

import urllib.request as httpc
from bs4 import BeautifulSoup

import json

from musicpd import (MPDClient, CommandError)

import paho.mqtt.client as mqtt

import curses
from curses.textpad import Textbox, rectangle
from datetime import datetime
from curses import wrapper

import showtimestamp
import showmpd
import showtraffic

def main(stdscr):
    global isopen
    global aussenAn
    global innenAn
    global vorneAn
    global trafficw
    isopen = False
    aussenAn = False
    innenAn = False
    vorneAn = False
    blank = False
    
    trafficw = showtraffic.trafficwin(1,11,76,14)

    def on_message(client, userdata, message):
        global isopen
        global aussenAn
        global innenAn
        global vorneAn
        global trafficw

        if (message.topic == "traffic/departures"):
            trafficw.update(json.loads(message.payload.decode("utf-8")))
        elif (message.topic == "club/status"):
            if (message.payload[0] != 0):
                isopen = True
            else:
                isopen = False
        elif (message.topic == "licht/keller/aussen"):
            if (message.payload[0] != 0):
                aussenAn = True
            else:
                aussenAn = False
        elif (message.topic == "licht/keller/vorne"):
            if (message.payload[0] != 0):
                vorneAn = True
            else:
                vorneAn = False
        elif (message.topic == "licht/keller/innen"):
            if (message.payload[0] != 0):
                innenAn = True
            else:
                innenAn = False

    mqttc=mqtt.Client()
    mqttc.connect("172.23.23.110",1883,60)
    mqttc.loop_start()

    mqttc.on_message = on_message
    mqttc.subscribe([("traffic/departures",2),("club/status",2),("licht/keller/aussen",2),("licht/keller/innen",2),("licht/keller/vorne",2)])

    mclient = MPDClient()
    
    timew = showtimestamp.timewin(1,1,13,5)
    mpdw = showmpd.mpdwin(1,6,76,5,"localhost")

    curses.curs_set(False)
    statuswin = curses.newwin(1,20,2,25)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    i = 0
    while True:
        timew.show()
        mpdw.show()
        statuswin.erase()
        if (isopen):
            statuswin.addstr(0,0, "Club is open!", curses.color_pair(2))
        else:
            statuswin.addstr(0,0, "Club is closed!", curses.color_pair(1))
        trafficw.show()
        statuswin.refresh()
        time.sleep(0.1)
        if (not vorneAn and not aussenAn and not innenAn and not blank):
            blank = True
            os.system("setterm --blank force --powersave on")
            #os.system("setterm --powersave powerdown")
        elif ((vorneAn or aussenAn or innenAn) and blank):
            blank = False
            os.system("setterm --blank poke")
            os.system("setterm --blank 0")

if __name__ == "__main__":
    wrapper(main)
