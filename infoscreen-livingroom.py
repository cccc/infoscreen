#!/usr/bin/env python3

import os
import curses

import showstatus
import showtimestamp
import showtemp
import showbikes
import showmpd
import showtraffic
import showheartbeat
import showsky
import dosockets

from infoscreen import Infoscreen

class Livingroom(Infoscreen):

    mpd_name = 'baellebad'

    def _init_windows(self):
        
        ### This should be it's own daemon!
        socket = dosockets.sockets()
        self.add_window(None,[
                {
                    "subscribe" : ("socket/wohnzimmer/+/+",2),
                    "callback"  : lambda message: socket.update(message.topic, message.payload),
                    "custom"    : True
                }
            ])

        statusw = showstatus.statuswin(1,2,29,1)
        self.add_window(statusw,[{
                "subscribe" : ("club/status",2),
                "callback"  : statusw.update,
                "json"      : False,
                "utf8"      : False
            }])
        
        timew = showtimestamp.timewin(1,4,13,4)
        self.add_window(timew,[])
        
        tempw = showtemp.tempwin(17, 4, 13, 4, "28-000008a0fd0b")
        self.add_window(tempw,[])
        
        bikesw = showbikes.bikeswin(33,1,44,9)
        self.add_window(bikesw,[{
                "subscribe" : ("bikes/nextbike",2),
                "callback"  : bikesw.update
            }])
        
        mpdw = showmpd.mpdwin(1,10,76,4)
        self.add_window(mpdw,[{
                "subscribe" : ("mpd/{}/state".format(self.mpd_name),2),
                "callback"  : mpdw.update_state,
                "json"      : False
            },
            {
                "subscribe" : ("mpd/{}/song".format(self.mpd_name),2),
                "callback"  : mpdw.update_song,
                "json"      : False
            }])
        
        trafficw = showtraffic.trafficwin(1,14,76,19)
        self.add_window(trafficw,[{
                "subscribe" : ("traffic/departures",2),
                "callback"  : trafficw.update
            }])
        
        hbw = showheartbeat.heartbeatwin(79,11,28,22)
        self.add_window(hbw,[
                {
                    "subscribe" : ("heartbeat/#",2),
                    "callback"  : lambda message: hbw.update(message.topic, message.payload),
                    "custom"    : True
                }
            ])
        
        skyw = showsky.skywin(79,1,28,10)
        self.add_window(skyw,[
                {
                    "subscribe" : ("skynet",2),
                    "listen"    : "skynet",
                    "callback"  : skyw.update
                }
            ])


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
