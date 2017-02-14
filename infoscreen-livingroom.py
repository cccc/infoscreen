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
    global isOn
    isopen = False
    blank = False
    isOn = dict()
    isOn['tuer'] = False
    trafficw = showtraffic.trafficwin(1,11,76,20)
    global trafficw
    
    def on_message(client, userdata, message):
        global isopen
        global isOn
        global trafficw
        if (message.topic == "traffic/departures"):
            trafficw.update(json.loads(message.payload))
        elif (message.topic == "club/status"):
            if (message.payload[0] != 0):
                isopen = True
            else:
                isopen = False
        elif (message.topic == "licht/wohnzimmer/tuer"):
            isOn['tuer'] = (message.payload[0] != 0)
            mqttc=mqtt.Client()
    mqttc=mqtt.Client()
    mqttc.connect("172.23.23.110",1883,60)
    mqttc.loop_start()

    mqttc.on_message = on_message
    mqttc.subscribe([("traffic/departures",2), ("club/status",2),("licht/wohnzimmer/+",2)])

    mclient = MPDClient()
    
    timew = showtimestamp.timewin(1,1,13,5)
    mpdw = showmpd.mpdwin(1,6,76,5,'autoc4')

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
        if (i == 50):
            i = 0
            trafficw.show()
        else:
            i += 1
        statuswin.refresh()
        time.sleep(0.1)
        if (not isOn['tuer'] and not blank):
            blank = True
            os.system("setterm --blank force --powersave on")
            #os.system("setterm --powersave powerdown")
        elif ((isOn['tuer']) and blank):
            blank = False
            os.system("setterm --blank poke")
            os.system("setterm --blank 0")

if __name__ == "__main__":
    wrapper(main)
