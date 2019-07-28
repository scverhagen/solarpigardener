#!/usr/bin/python3

import os
import socket

from app import forms
from app import config

def get_ip():
    # strange hack to get local ip address:
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


from flask import Flask, request, send_file, render_template, redirect, url_for, session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'garDener_debuG_seCret'


app.config.update(
    #CELERY_BROKER_URL='redis://' + get_ip() + ':6379'
    CELERY_BROKER_URL='redis://redis:6379'
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

import app.gardener_fx as gardener_fx

import app.gardener_controls as gardener_controls
control_waterpump = gardener_controls.water_pump()

@celery.task()
def do_water_for(secs):
    control_waterpump.water_for(secs)
    
@app.route('/controls')
def www_controls():
    if not session.get('logged_in'):
        return render_template('access_denied.html')

    return render_template('controls.html')
    
@app.route('/controls_pump')
def www_controls_pump():
    if not session.get('logged_in'):
        return render_template('access_denied.html')
    
    return render_template('controls_pump.html')
    
@app.route('/schedule')
def www_schedule():
        return render_template('schedule.html')
 
@app.route('/pump')
def www_pump():
    if not session.get('logged_in'):
        return render_template('access_denied.html')
        
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
    if os.path.exists(config.settingsjsonpath):
        g_settings = config.loadSettings()
        return render_template('index.html', g_settings=g_settings)
    else:
        return www_config()

@app.route('/config', methods=["GET","POST"])
def www_config():
    firstrun = False
    if not session.get('logged_in') and os.path.exists(config.settingsjsonpath):
        return render_template('access_denied.html')
    
    if not os.path.exists(config.settingsjsonpath):
        firstrun = True
    
    g_settings = config.loadSettings()
    form = forms.ConfigForm(obj=g_settings)
    if form.validate_on_submit():
        old_password = g_settings.admin_password
        form.populate_obj(g_settings)
        
        # use old password if none specified:
        if g_settings.admin_password == '':
            session.clear()
            g_settings.admin_password = old_password

        # save configuration
        config.saveSettings(g_settings)
        if len(g_settings.redirect_url) > 0:
            return redirect( g_settings.redirect_url )
        else:
            return redirect( url_for('www_root') )
    
    return render_template('config.html', form=form, firstrun=firstrun, build_date=config.BUILD_DATE, commit_id=config.COMMIT_ID)

@app.route('/login', methods=["GET","POST"])
def www_login():
    g_settings = config.loadSettings()
    form = forms.LoginForm()
    if form.validate_on_submit():
        if form.password.data == g_settings.admin_password:
            session['logged_in'] = True
 
        if len(g_settings.redirect_url) > 0:
            return redirect( g_settings.redirect_url )
        else:
            return redirect( url_for('www_root') )

    return render_template('login.html', form=form)

@app.route('/logoff', methods=["GET"])
def www_logoff():
    session.clear()
    
    return redirect( url_for('www_root') )

#needs to be at end of file:
if __name__ == '__main__':
    app.run(debug=True,port=5000)
