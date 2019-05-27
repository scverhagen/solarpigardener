import os
import json

thisfilepath = os.path.dirname(__file__)

global defaultsettingsdict
defaultsettingsdict = {'water_application_inches_per_week':2, 'sprinkler_inches_per_minute':0.075, 'auto_schedule_water':0, 'url_video_feed':''}

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
        