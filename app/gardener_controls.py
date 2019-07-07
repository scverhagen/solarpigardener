#!/usr/bin/python3
import os
import sys
import platform
import time
from flask import Flask
import gpiozero
from celery import Celery
from gpiozero.pins.pigpio import PiGPIOFactory
import app

import app.gardener_settings as gardener_settings

is_pi = (platform.machine() == 'armv7l')
IN_DOCKER = False
docker_env = os.environ.get('IN_DOCKER', False)
if docker_env:
    print('Running in docker container.')
    IN_DOCKER = True

factory = PiGPIOFactory('solarpi.lan')
#if IN_DOCKER:
    #this currently does not work in older docker versions:
    #factory = PiGPIOFactory('host.docker.internal')

pin_moisture_sensor = 20
pin_water_solenoid = 21
pin_5v_solenoid = 26

class water_pump(object):
    def __init__(self):
        self.state = 0
        self.solenoid = gpiozero.LED(pin_water_solenoid, pin_factory=factory)
        self.solenoid.off()
        
    def On(self):
        self.state = 1
        self.solenoid.on()
        
    def Off(self):
        self.state = 0
        self.solenoid.off()
                    
    def water_for(self, secs):
            self.solenoid.on()
            time.sleep(secs)
            self.solenoid.off()
            
class acc_5v_power(object):
    def __init__(self):
        self.state = 0
        self.solenoid = gpiozero.LED(pin_5v_solenoid, pin_factory=factory)
        self.solenoid.off()
        
    def On(self):
        self.state = 1
        self.solenoid.on()
        
    def Off(self):
        self.state = 0
        self.solenoid.off()
            
            