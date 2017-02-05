#!/usr/bin/env python3

import time

from musicpd import (MPDClient, CommandError)

import paho.mqtt.client as mqtt

import curses
from curses.textpad import Textbox, rectangle
from datetime import datetime
from curses import wrapper

def main(stdscr):
    global isopen
    isopen = False
    
    def on_message(client, userdata, message):
        global isopen
        if (message.topic == "club/status"):
            if (message.payload[0] != 0):
                isopen = True
            else:
                isopen = False

    mqttc=mqtt.Client()
    mqttc.connect("172.23.23.110",1883,60)
    mqttc.loop_start()

    mqttc.on_message = on_message
    mqttc.subscribe("club/status",2)

    mclient = MPDClient()
    
    timewin = curses.newwin(5,30, 1,1)
    statuswin = curses.newwin(1,20,1,25)
    mpdwin = curses.newwin(6,70, 7, 1)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
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
        rectangle(mpdwin,1,0,3,59)
        try:
            mclient.connect("localhost", 6600)
            mpdwin.addstr(2,2,mclient.currentsong().get('file',0))
            mclient.disconnect()
        except SocketError:
            mpdwin.addstr(2,2,"Keine Verbindung zum MPD!", curses.color_pair(1));
        timewin.refresh()
        statuswin.refresh()
        mpdwin.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    wrapper(main)
