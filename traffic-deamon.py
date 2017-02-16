#!/usr/bin/env python3

import time

import urllib.request as httpc
from bs4 import BeautifulSoup

import json

import paho.mqtt.client as mqtt

class trafficd:
    def __init__(self, vrsurla, vrsurlb, kvburl):
       self.vrsurla = vrsurla
       self.vrsurlb = vrsurlb
       self.kvburl = kvburl

    def get_json(self, url):
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

    def get_time(self, dep):
        return (dep['estimate'] if 'estimate' in dep else dep['timetable'])

    def time_to_sec(self, t):
        return (int)(t[0:2])*3600 + (int)(t[3:5])*60 #+ ((int)(t[6:8]) if len(t) >= 8 else 0)

    def get_departures(self):
        result = {}
        result['departures'] = []
        try:
            ubtable = self.get_json(self.vrsurla)
            bhftable = self.get_json(self.vrsurlb)
            result['srvtime'] = bhftable['updated']
            srvtime = self.time_to_sec(result['srvtime'][7:16])
            ubtable = ubtable['events']
            bhftable = bhftable['events']
            ubc = 0
            bhfc = 0
            for s in range(0,len(ubtable)+len(bhftable)):
                nextdep = {}
                if (ubc < len(ubtable)):
                    ubdeptime = self.time_to_sec(self.get_time(ubtable[ubc]['departure']))
                    if (ubdeptime < srvtime and (srvtime-ubdeptime) > 12*3600):
                        ubdepmin = (((24*3600)-srvtime)+ubdeptime)/60
                    else:
                        ubdepmin = abs(ubdeptime-srvtime)/60
                if (bhfc < len(bhftable)):
                    bhfdeptime = self.time_to_sec(self.get_time(bhftable[bhfc]['departure'])) 
                    if (bhfdeptime < srvtime and (srvtime-bhfdeptime) > 12*3600):
                        bhfdepmin = (((24*3600)-srvtime)+bhfdeptime)/60
                    else:
                        bhfdepmin = (bhfdeptime-srvtime)/60
                if (ubc < len(ubtable) and (bhfc >= len(bhftable) or ubdepmin < bhfdepmin)):
                    depmin = ubdepmin
                    deptime = ubdeptime
                    dep = ubtable[ubc]['departure']
                    line = ubtable[ubc]['line']
                    ubc = ubc+1
                elif (bhfc < len(bhftable)):
                    depmin = bhfdepmin
                    deptime = bhfdeptime
                    dep = bhftable[bhfc]['departure']
                    line = bhftable[bhfc]['line']
                    bhfc = bhfc+1
                else:
                    break
                nextdep['line'] = line['number']
                nextdep['direction'] = line['direction']
                nextdep['reldeparture'] = depmin
                nextdep['departure'] = self.get_time(dep) 
                nextdep['timetable'] = dep['timetable']
                if ('estimate' in dep and 'timetable' in dep):
                    timetabletime = self.time_to_sec(dep['timetable'])
                    if (deptime < timetabletime and (timetabletime-deptime) > 12*3600):
                        delaytime = deptime + ((24*3600)-timetabletime)
                    else:
                        delaytime = deptime - timetabletime
                    delaytime = delaytime/60
                    nextdep['delay'] = delaytime
                result['departures'].append(nextdep)
        except:
            req = httpc.Request(
                    self.kvburl, 
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
            result['srvtime'] = lines[0][0]
            lines = lines[1:len(lines)]
            for s,(line,destination,departure) in enumerate(lines):
                nextdep = {'line': line, 'direction': destination, 'reldeparture': departure}
                result['departures'].append(nextdep)
        return result

if __name__ == "__main__":
    mqttc=mqtt.Client()
    mqttc.connect("172.23.23.110",1883,60)
    mqttc.loop_start()
    trfc = trafficd( "https://www.vrsinfo.de/index.php?eID=tx_vrsinfo_ass2_departuremonitor&i=LEbuNjirOBzyGfCXaM9GxZQ47Dq8S4ET",
            "https://www.vrsinfo.de/index.php?eID=tx_vrsinfo_ass2_departuremonitor&i=N5Kq9iKszPov29W46gjTFoILylOK86zL",
            "http://www.kvb-koeln.de/generated/?aktion=show&code=251&title=none"
            )
    while (True):
        mqttc.publish("traffic/departures", json.dumps(trfc.get_departures()), 2)
        time.sleep(5)

