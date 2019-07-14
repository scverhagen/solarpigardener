#!/usr/bin/python3

import os
import json

thisfilepath = os.path.dirname(__file__)

IN_DOCKER = False
docker_env = os.environ.get('IN_DOCKER', False)
if docker_env:
    print('Running in docker container.')
    IN_DOCKER = True


class Settings(object):
    def __init__(self, hardware_water_gpio_pin = 21, water_inches_per_week = 2, water_days_per_week = 2, water_time_hour = 6, sprinkler_inches_per_minute = "0.00418", enable_auto_watering = 0, submit = None):
        self.hardware_water_gpio_pin = hardware_water_gpio_pin
        self.water_inches_per_week = water_inches_per_week
        self.water_days_per_week = water_days_per_week
        self.water_time_hour = water_time_hour
        self.sprinkler_inches_per_minute = sprinkler_inches_per_minute
        self.enable_auto_watering = enable_auto_watering

    def to_json(self):
        return json.dumps(self.__dict__)
        
    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

def saveSettings(g_settings):
    settingsjsonpath = os.path.join(thisfilepath, 'gardener_settings.json')
    json = g_settings.to_json()
    with open(settingsjsonpath , 'w') as file:
        file.write(json)
    
def loadSettings():
    settingsjsonpath = os.path.join(thisfilepath, 'gardener_settings.json')
    g_settings = Settings()

    # if gardener_settings.json file exists, load settings from json, otherwise, load default settings:
    if os.path.exists(settingsjsonpath):
        with open(settingsjsonpath, 'r') as file:
            data = file.read()
            this_json = json.loads(json.dumps(data))
            g_settings = g_settings.from_json(this_json)
    return g_settings