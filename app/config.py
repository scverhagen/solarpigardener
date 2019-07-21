#!/usr/bin/python3

import os
import json

thisfilepath = os.path.dirname(__file__)
settingsjsonpath = os.path.join(thisfilepath, 'gardener_settings.json')

IN_DOCKER = False
BUILD_DATE = "n/a"
docker_env = os.environ.get('IN_DOCKER', False)
if docker_env:
    print('Running in docker container.')
    settingsjsonpath = '/etc/gardener/gardener.conf'
    IN_DOCKER = True
    with open('/build_date.txt', 'r') as f:
        BUILD_DATE = f.readline()
    print('BUILD DATE:  ' + BUILD_DATE)

class Settings(object):
    def __init__(self, hardware_water_gpio_pin = 21, water_inches_per_week = 2, water_days_per_week = 2, water_time_hour = 6, sprinkler_inches_per_minute = "0.00418", enable_auto_watering = 0, submit = None, admin_password = '', redirect_url='http://solarpi'):
        self.hardware_water_gpio_pin = hardware_water_gpio_pin
        self.water_inches_per_week = water_inches_per_week
        self.water_days_per_week = water_days_per_week
        self.water_time_hour = water_time_hour
        self.sprinkler_inches_per_minute = sprinkler_inches_per_minute
        self.enable_auto_watering = enable_auto_watering
        self.admin_password = admin_password
        self.redirect_url = redirect_url

    def to_json(self):
        return json.dumps(self.__dict__)
        
    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

def saveSettings(g_settings):
    json = g_settings.to_json()
    print('Saving config to: ' + settingsjsonpath)
    with open(settingsjsonpath , 'w') as file:
        file.write(json)
    
def loadSettings():
    g_settings = Settings()

    # if gardener_settings.json file exists, load settings from json, otherwise, load default settings:
    if os.path.exists(settingsjsonpath):
        with open(settingsjsonpath, 'r') as file:
            data = file.read()
            this_json = json.loads(json.dumps(data))
            g_settings = g_settings.from_json(this_json)
    return g_settings