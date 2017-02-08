#!/usr/bin/env python3

import time

import urllib.request as httpc
from bs4 import BeautifulSoup

import json

import curses
from curses.textpad import Textbox, rectangle
from datetime import datetime
from curses import wrapper

kvburl = "http://www.kvb-koeln.de/generated/?aktion=show&code=251&title=none"
vrsbhfurl = "https://www.vrsinfo.de/index.php?eID=tx_vrsinfo_ass2_departuremonitor&i=LEbuNjirOBzyGfCXaM9GxZQ47Dq8S4ET"
vrsuburl = "https://www.vrsinfo.de/index.php?eID=tx_vrsinfo_ass2_departuremonitor&i=N5Kq9iKszPov29W46gjTFoILylOK86zL"

def get_json(url):
    req = httpc.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )

    f = httpc.urlopen(req)
    res = f.read().decode('utf8')
    return json.loads(res)

def get_time(dep):
    return (dep['estimate'] if 'estimate' in dep else dep['timetable'])



class trafficwin:
    def __init__(self, xpos, ypos, width, height):
        self.win = curses.newwin(height,width, ypos, xpos)
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos

    def show(self):
        self.win.erase()
        rectangle(self.win,1,0,self.height-2,self.width-1)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLUE)

        try:
            ubtable = get_json(vrsuburl)
            bhftable = get_json(vrsbhfurl)
            ubtimestr = ubtable['updated']
            bhftimestr = bhftable['updated']
            ubtime = datetime.strptime("2017 "+ubtimestr[7:15], '%Y %H:%M:%S').timestamp()
            bhftime = datetime.strptime("2017 "+bhftimestr[7:15], '%Y %H:%M:%S').timestamp()
            self.win.addstr(0,0, "Departures "+ubtable['updated'])
            ubtable = ubtable['events']
            bhftable = bhftable['events']
            ubc = 0
            bhfc = 0
            for s in range(0,self.height-4):
                if (ubc < len(ubtable) and get_time(ubtable[ubc]['departure']) < get_time(bhftable[bhfc]['departure'])):
                    dep = ubtable[ubc]['departure']
                    line = ubtable[ubc]['line']
                    ubc = ubc+1
                    utime = ubtime
                elif (bhfc < len(bhftable)):
                    dep = bhftable[bhfc]['departure']
                    line = bhftable[bhfc]['line']
                    utime = bhftime
                    bhfc = bhfc+1
                else:
                    break
                self.win.addstr(2+s,2,' '*(self.width-3), curses.color_pair(0 if (s%2)==0 else 3))
                self.win.addstr(2+s,2,(line['number']+'\t'+line['direction'])[0:self.width-21], curses.color_pair(0 if (s%2)==0 else 3))
                deptime = datetime.strptime("2017 "+get_time(dep), '%Y %H:%M').timestamp()
                depmin = abs(deptime-utime)/60
                self.win.addstr(2+s,self.width-20,("%d Min." % depmin if depmin > 1 else "Sofort"),curses.color_pair(0 if (s%2)==0 else 3))
                if ('estimate' in dep and 'timetable' in dep):
                    delaytime = deptime - datetime.strptime("2017 "+dep['timetable'], '%Y %H:%M').timestamp()
                    delaytime = abs(delaytime)/60
                    if (delaytime > 1):
                        self.win.addstr(2+s,self.width-10,"(+%d Min)" % delaytime,curses.color_pair(1 if (s%2)==0 else 4))
                    else:
                        self.win.addstr(2+s,self.width-10,"(+0 Min)",curses.color_pair(2 if (s%2)==0 else 5))

        except:
            req = httpc.Request(
                    kvburl, 
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
            self.win.addstr(0,0, "Abfahrten "+lines[0][0])
            lines = lines[1:11]
            for s,(line,destination,departure) in enumerate(lines):
                self.win.addstr(2+s,2,line+'\t'+destination)
                self.win.addstr(2+s,60,departure)


        self.win.refresh()

