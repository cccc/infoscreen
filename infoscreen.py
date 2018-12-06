#!/usr/bin/env python3

import json
import time
import sys
import re
from threading import Lock
import paho.mqtt.client as mqtt
from paho.mqtt.client import topic_matches_sub

class Infoscreen():

    mqtt_host = "autoc4"
    mqtt_port = 1883
    mqtt_keepalive = 60

    def __init__(self, clientid, stdscr):

        # self.is_on = { 'tuer' : False }
        self.blank = False
        self.stdscr = stdscr
        self.lock = Lock()
        
        self.registered_windows = list()

        self._init_windows()
        self._init_mqtt(clientid)

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
                    listener["subscribe"]
                    for registration in self.registered_windows
                    for listener in registration["listeners"]
                ])

            self.mqttc.publish(self.heartbeat_topic, bytearray(b'\x01'), 2, retain=True)
    
    def add_window(self, window, listeners):
        self.registered_windows.append({
                "window":window,
                "listeners": [
                        {
                            "custom"    : listener["custom"] if "custom" in listener else False,
                            "subscribe" : listener["subscribe"] if "subscribe" in listener else None,
                            "json"      : listener["json"] if "json" in listener else True,
                            "utf8"      : listener["utf8"] if "utf8" in listener else True,
                            "callback"  : listener["callback"]
                        }
                        
                        for listener in listeners
                    ]
            })
        
    
    def on_message(self, client, userdata, message):

        self.lock.acquire()
        
        try:
            for registration in self.registered_windows:
                for listener in registration["listeners"]:
                    if topic_matches_sub(listener["subscribe"][0], message.topic):
                        if listener["custom"]:
                            listener["callback"](message)
                        else:
                            payload = message.payload
                            if listener["json"]:
                                try:
                                    payload = json.loads(message.payload.decode("utf-8"))
                                except Exception as msg:
                                    print("An error occured while parsing JSON for topic \"%s\" : %s" % (message.topic, str(msg)) )
                            elif listener["utf8"]:
                                payload = message.payload.decode("utf-8")
                            listener["callback"](payload)
        except Exception as msg:
            print(msg)

        self.lock.release()

        # elif (message.topic == "licht/wohnzimmer/tuer"):
        #     self.is_on['tuer'] = (message.payload[0] != 0)

    def run(self):

        while True:

            self.lock.acquire()
            
            self.stdscr.clear()
            for registration in self.registered_windows:
                if registration["window"] is not None:
                    registration["window"].show()
                
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
