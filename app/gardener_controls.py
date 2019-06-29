#!/usr/bin/python3
import os
import sys
import platform
import time

is_pi = (platform.machine() == 'armv7l')

if is_pi:
    import gpiozero

pin_moisture_sensor = 20
pin_water_solenoid = 21
pin_5v_solenoid = 26

class water_pump(object):
    def __init__(self):
        self.state = 0
        if is_pi:
            self.solenoid = gpiozero.LED(pin_water_solenoid)
            self.solenoid.off()
        else:
            self.solenoid = None
        
    def On(self):
        self.state = 1
        if is_pi:
            self.solenoid.on()
        
    def Off(self):
        self.state = 0
        if is_pi:
            self.solenoid.off()
                    
    def water_for(self, secs):
        pid = os.fork()
        if pid == 0:
            # child process:
            if is_pi:
                self.solenoid.on()
            time.sleep(secs)
            if is_pi:
                self.solenoid.off()
            os._exit(0)
            
class acc_5v_power(object):
    def __init__(self):
        self.state = 0
        if is_pi:
            self.solenoid = gpiozero.LED(pin_5v_solenoid)
            self.solenoid.off()
        else:
            self.solenoid = None
        
    def On(self):
        self.state = 1
        if is_pi:
            self.solenoid.on()
        
    def Off(self):
        self.state = 0
        if is_pi:
            self.solenoid.off()
            
            