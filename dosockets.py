
import RPi.GPIO as GPIO

class sockets:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22,GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)
        GPIO.output(22,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)

    def update(self,topic,payload):
        if (topic == "socket/wohnzimmer/screen/a"):
            if (payload[0] != 0): 
                GPIO.output(22,GPIO.HIGH)
            else:
                GPIO.output(22,GPIO.LOW)
        if (topic == "socket/wohnzimmer/screen/b"):
            if (payload[0] != 0): 
                GPIO.output(23,GPIO.HIGH)
            else:
                GPIO.output(23,GPIO.LOW)
