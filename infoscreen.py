#!/usr/bin/env python3

import json
import time
import sys
from threading import Lock
import paho.mqtt.client as mqtt


class Infoscreen():

    mqtt_host = "172.23.23.110"
    mqtt_port = 1883
    mqtt_keepalive = 60

    mpd_name = None

    def __init__(self, clientid, stdscr):

        # self.is_on = { 'tuer' : False }
        self.blank = False
        self.stdscr = stdscr
        self.lock = Lock()

        self._init_mqtt(clientid)
        self._init_windows()

    def _init_mqtt(self, clientid):

        self.heartbeat_topic = "heartbeat/" + clientid

        self.mqttc = mqtt.Client(clientid)
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.will_set(self.heartbeat_topic, bytearray(b'\x00'), 2, True)

        self.mqttc.connect(self.mqtt_host, self.mqtt_port, self.mqtt_keepalive)

        self.mqttc.loop_start()

    def _init_windows(self):

        raise NotImplementedError('Abstract method')

    def on_connect(self, a, b, c, rc):

        if rc != 0:
            sys.exit(1) # connect failed # TODO

        else:

            self.mqttc.subscribe([
                    ("traffic/departures",             2),
                    ("heartbeat/#",                    2),
                    ("club/status",                    2),
                    ("licht/wohnzimmer/+",             2),
                    ("skynet",                         2),
                    ("mpd/{}/+".format(self.mpd_name), 2),
                    ("socket/wohnzimmer/+/+",            2),
                ])

            self.mqttc.publish(self.heartbeat_topic, bytearray(b'\x01'), 2, retain=True)
    
    def on_message(self, client, userdata, message):

        self.lock.acquire()

        if (message.topic == "traffic/departures"):
            self.trafficw.update(json.loads(message.payload.decode("utf-8")))

        elif (message.topic == "skynet"):
            self.skyw.update(json.loads(message.payload.decode("utf-8")))

        elif (message.topic == "mpd/{}/state".format(self.mpd_name)):
            self.mpdw.update_state(message.payload.decode("utf-8"))

        elif (message.topic == "mpd/{}/song".format(self.mpd_name)):
            self.mpdw.update_song(message.payload.decode("utf-8"))

        elif (message.topic == "club/status"):
            self.statusw.update(message.payload)

        elif (message.topic.startswith("heartbeat/")):
            self.hbw.update(message.topic, message.payload)

        elif (message.topic.startswith("socket/wohnzimmer/screen/")):
            self.socket.update(message.topic,message.payload)

        self.lock.release()

        # elif (message.topic == "licht/wohnzimmer/tuer"):
        #     self.is_on['tuer'] = (message.payload[0] != 0)

    def run(self):

        while True:
            self.lock.acquire()
            self.stdscr.clear()
            self.timew.show()
            self.tempw.show()
            self.mpdw.show()
            self.trafficw.show()
            self.statusw.show()
            self.hbw.show()
            self.skyw.show()
            self.lock.release()
            time.sleep(0.1)

#        if (not isOn['tuer'] and not blank):
#            blank = True
#            os.system("setterm --blank force --powersave on")
#            #os.system("setterm --powersave powerdown")
#        elif ((isOn['tuer']) and blank):
#            blank = False
#            os.system("setterm --blank poke")
#            os.system("setterm --blank 0")
