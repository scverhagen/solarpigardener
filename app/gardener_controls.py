#!/usr/bin/python3
import os
import sys
import platform
import time
import gpiozero

import app.gardener_settings as gardener_settings

is_pi = (platform.machine() == 'armv7l')

pin_moisture_sensor = 20
pin_water_solenoid = 21
pin_5v_solenoid = 26

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
                    
    def water_for(self, secs):
        pid = os.fork()
        if pid == 0:
            # child process:
            self.solenoid.on()
            time.sleep(secs)
            self.solenoid.off()
            os._exit(0)
            
class acc_5v_power(object):
    def __init__(self):
        self.state = 0
        self.solenoid = gpiozero.LED(pin_5v_solenoid)
        self.solenoid.off()
        
    def On(self):
        self.state = 1
        self.solenoid.on()
        
    def Off(self):
        self.state = 0
        self.solenoid.off()
            
            