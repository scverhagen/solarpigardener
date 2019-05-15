#!/usr/bin/python3
import os
import sys
import time

import gpiozero

pin_moisture_sensor = 20
pin_water_solenoid = 21

class water_pump(object):
    def __init__(self):
        self.state = 0
        self.solenoid = gpiozero.LED(pin_water_solenoid)
        self.solenoid.off()
        
    def On(self):
        self.state = 1
        self.solenoid.on()
        
    def Off(self):
        self.state = 0
        self.solenoid.off()
        
    def Toggle(self):
        if self.state == 0:
            self.state = 1
            self.on()
        else:
            self.state = 0
            self.off()
            
    def water_for(self, secs):
        pid = os.fork()
        if pid != 0:
            # child process:
            self.solenoid.on()
            time.sleep(secs)
            self.solenoid.off()
            sys.exit(0)