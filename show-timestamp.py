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

def main(stdscr):
    global isopen
    global aussenAn
    global innenAn
    global vorneAn
    isopen = False
    aussenAn = False
    innenAn = False
    vorneAn = False
    blank = False
    
    def on_message(client, userdata, message):
        global isopen
        global aussenAn
        global innenAn
        global vorneAn
        if (message.topic == "club/status"):
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


    url = "http://www.kvb-koeln.de/generated/?aktion=show&code=251&title=none"

    mqttc=mqtt.Client()
    mqttc.connect("172.23.23.110",1883,60)
    mqttc.loop_start()

    mqttc.on_message = on_message
    mqttc.subscribe([("club/status",2),("licht/keller/aussen",2),("licht/keller/innen",2),("licht/keller/vorne",2)])

    mclient = MPDClient()
    
    timewin = curses.newwin(5,30, 1,1)
    statuswin = curses.newwin(1,20,2,25)
    mpdwin = curses.newwin(6,70,6, 1)
    kvbwin = curses.newwin(12,45,13,1)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    i = 0
    while True:
        timewin.erase()
        statuswin.erase()
        mpdwin.erase()
        timewin.addstr(0, 0, "Current time:")
        rectangle(timewin, 1,0, 3, 11)
        timewin.addstr(2,2, "{:%H:%M:%S}".format(datetime.now()))
        if (isopen):
            statuswin.addstr(0,0, "Club is open!", curses.color_pair(2))
        else:
            statuswin.addstr(0,0, "Club is closed!", curses.color_pair(1))
        mpdwin.addstr(0,0, "Now Playing:")
        rectangle(mpdwin,1,0,4,69)
        try:
            mclient.connect("localhost", 6600)
            mpdwin.addstr(2,2,mclient.currentsong().get('file',0))
            mclient.disconnect()
        except SocketError:
            mpdwin.addstr(2,2,"Keine Verbindung zum MPD!", curses.color_pair(1));
        if (i == 10):
            i = 0
            req = httpc.Request(
                    url, 
                    data=None, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                        }
                    )

            f = httpc.urlopen(req)
            html = f.read().decode('iso8859_15')
            soup = BeautifulSoup(html)
            for script in soup(["script", "style"]):
                script.extract()
            lines = [[col.get_text().strip() for col in row.find_all("td")] for row in soup.find_all("tr")]
            kvbwin.erase()
            kvbwin.addstr(0,0, "Abfahrten "+lines[0][0])
            rectangle(kvbwin,1,0,10,44)
            lines = lines[1:9]
            for s,(line,destination,departure) in enumerate(lines):
                kvbwin.addstr(2+s,2,line+'\t'+destination)
                kvbwin.addstr(2+s,35,departure)
        else:
            i += 1
        kvbwin.refresh()
        timewin.refresh()
        statuswin.refresh()
        mpdwin.refresh()
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
