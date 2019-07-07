#!/usr/bin/python3

import os
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


from flask import Flask, request, send_file, render_template
app = Flask(__name__)


app.config.update(
    CELERY_BROKER_URL='redis://' + get_ip() + ':6379'
    #CELERY_RESULT_BACKEND='redis://' + get_ip() + ':6379'
)

from celery import Celery
def make_celery(app):
    celery = Celery(
        app.import_name,
        #backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


import app.gardener_settings as gardener_settings
settings = gardener_settings.settings()

import app.gardener_fx as gardener_fx

import app.gardener_controls as gardener_controls
control_waterpump = gardener_controls.water_pump()

def process_gardener_command(gc):
    lcmd = gc.lower()
    args = gc.split()
    argc = len(args)
    largs = lcmd.split()
    
    if largs[0] == 'water_pump_on':
        control_waterpump.On()
    elif largs[0] == "system_reboot":
        print('Rebooting system...')
        os.system("reboot")
    elif largs[0] == "system_poweroff":
        print('Powering system OFF...')
        os.system("poweroff");
    elif largs[0] == "ping":
        print('ping')
    elif largs[0] == "check_moisture":
        #update_params_moisture_sensor()
        print("Moisture param updated.")
    elif largs[0] == 'force_water':
        print("Forcing maintenance.")
        #gardener_do_maint();
    elif largs[0] == "kill_process":
        print("Killing Process.")
        sys.exit(1)
    elif largs[0] == 'water_for':
        if argc > 1:
            duration = largs[1]
            control_waterpump.water_for(int(duration))



@celery.task()
def do_water_for(secs):
    control_waterpump.water_for(secs)
    
    

@app.route('/controls')
def www_controls():
    return render_template('controls.html')

@app.route('/pump5')
def www_pump5():
    do_water_for.delay(5)
    return render_template('pump5.html')

@app.route('/favicon.ico')
def www_favicon():
    app.send_static_file('logo.img')

@app.route('/')
def www_root():
    return www_controls()

#needs to be at end of file:
if __name__ == '__main__':
    app.run(debug=True)
