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

@celery.task()
def do_water_for(secs):
    control_waterpump.water_for(secs)
    
@app.route('/controls')
def www_controls():
    return render_template('controls.html')

@app.route('/controls_pump')
def www_controls_pump():
    return render_template('controls_pump.html')

@app.route('/pump')
def www_pump():
    num_mins = request.args.get('mins')

    if num_mins == None:
        return 'An error has occurred.'
    else:
        num_mins = int(num_mins)
        
    num_secs = 60 * num_mins
    do_water_for.delay(num_secs)
    return render_template('pumpX.html', mins=str(num_mins))

@app.route('/favicon.ico')
def www_favicon():
    app.send_static_file('logo.img')

@app.route('/')
def www_root():
    return www_controls()

#needs to be at end of file:
if __name__ == '__main__':
    app.run(debug=True)
