#!/usr/bin/python3

import os
from flask import Flask, request, send_file, render_template
app = Flask(__name__)

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

@app.route('/controls')
def www_controls():
    return render_template('controls.html')

@app.route('/dashboard')
def www_dashboard():
    return render_template('index.html')

@app.route('/pump5')
def www_pump5():
    control_waterpump.water_for(5)
    return render_template('pump5.html')

@app.route('/favicon.ico')
def www_favicon():
    app.send_static_file('logo.img')

@app.route('/')
def www_root():
    return www_dashboard()

#needs to be at end of file:
if __name__ == '__main__':
    app.run(debug=True)
