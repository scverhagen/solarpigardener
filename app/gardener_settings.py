#!/usr/bin/python3

import os
import json

thisfilepath = os.path.dirname(__file__)

IN_DOCKER = False
docker_env = os.environ.get('IN_DOCKER', False)
if docker_env:
    print('Running in docker container.')
    IN_DOCKER = True

global defaultsettingsdict
defaultsettingsdict = {'water_application_inches_per_week':2, 'water_application_days_per_week':2 , 'sprinkler_inches_per_minute':0.00418, 'owm_key':'enter_key_here', 'url_video_feed':''}

class settings(object):
    def __init__(self):
        self.dict = {}
        self.load()

    def save(self):
        settingsjsonpath = os.path.join(thisfilepath, 'gardener_settings.json')
        with open(settingsjsonpath , 'w') as file:
            file.write(json.dumps(defaultsettingsdict))
            self.dict = defaultsettingsdict

    def load(self):
        settingsjsonpath = os.path.join(thisfilepath, 'gardener_settings.json')
        self.dict = {}

        # create settings .json file (using defaultsettingsdict as a template) if it does not already exist
        if os.path.exists(settingsjsonpath) == False:
            with open(settingsjsonpath , 'w') as file:
                file.write(json.dumps(defaultsettingsdict))
                self.dict = defaultsettingsdict
            os.chmod(settingsjsonpath, 0o777)
        else:
            # .json file exists, load it:
            with open(settingsjsonpath, 'r') as file:
                self.dict = json.load(file)
    def get(self, settingname):
        return self.dict[settingname]
    
    def set(self, settingname, settingval):
        self.dict[settingname] = settingval

class watering_schedule(object):
    datapath = os.path.join(thisfilepath, 'data')
    def __init__(self, fsettings):
        self.app_in_per_week = fsettings.get('water_application_inches_per_week')
        self.app_days_per_week = fsettings.get('water_application_days_per_week')
        self.app_in_per_day = self.app_in_per_week / self.app_days_per_week
        
        # create data dir if it does not exist:
        if os.path.exists(datapath) == False:
            os.mkdir(datapath)


if __name__ == '__main__':
    tmp_settings = settings()