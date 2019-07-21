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
from app import config

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

#pin_moisture_sensor = 20
#pin_water_solenoid = 21
#pin_5v_solenoid = 26

class water_pump(object):
    def __init__(self):
        self.state = 0
        g_settings = config.loadSettings()
        self.solenoid = gpiozero.LED(int(g_settings.hardware_water_gpio_pin), pin_factory=factory)
        self.solenoid.off()
        
    def On(self):
        self.state = 1
        g_settings = config.loadSettings()
        self.solenoid = gpiozero.LED(int(g_settings.hardware_water_gpio_pin), pin_factory=factory)
        self.solenoid.on()
        
    def Off(self):
        self.state = 0
        g_settings = config.loadSettings()
        self.solenoid = gpiozero.LED(int(g_settings.hardware_water_gpio_pin), pin_factory=factory)

        self.solenoid.off()
                    
    def water_for(self, secs):
            g_settings = config.loadSettings()
            self.state = 1
            self.solenoid = gpiozero.LED(int(g_settings.hardware_water_gpio_pin), pin_factory=factory)
            self.solenoid.on()
            time.sleep(secs)
            self.solenoid.off()
            self.state = 0
