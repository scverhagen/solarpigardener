#!/usr/bin/python3
import os
from flask import Flask, request, send_file, render_template
app = Flask(__name__)

import app.gardener_settings as gardener_settings
settings = gardener_settings.settings()

import app.gardener_fifo as gardener_fifo
import app.gardener_fx as gardener_fx

thisfilepath = os.path.dirname(__file__)
status_fifo = gardener_fifo.status_fifo()
command_fifo = gardener_fifo.command_fifo()

@app.route('/status')
def wwww_status():
    status_dict = status_fifo.getstatusdict()
    
    hs = html.html_start()
    hs += html.readfile('navbar')
    hs += '<div class="jumbotron">'
    hs += '<h3>Service</h3>'
    hs += """
    <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-center">
        """
    hs += 'Uptime<span class="badge badge-primary badge-pill">' + str( gardener_fx.time_to_text(status_dict['uptime'])) + '</span>'
    hs += """
        </li>
    </ul>
    """
    hs += "<br>"
    hs += '<h3>Power</h3>'
    hs += """
    <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-center">
        """
    hs += 'Battery Status<span class="badge badge-primary badge-pill">' + status_dict['bat_status'] + '</span>'
    hs += """
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
        """
    hs += 'Battery Voltage<span class="badge badge-primary badge-pill">' + str(status_dict['bat_voltage']) + ' V</span>'
    hs += """
        </li>
    </ul>
    """
    hs += '<br>'
    hs += '<h3>Readings</h3>'
    hs += """
    <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-center">
        """
    hs += 'Soil Moisture Reading<span class="badge badge-primary badge-pill">' + str(status_dict['moisture_reading']) + '%</span>'
    hs += """
        </li>
    </ul>
    """

    hs += '</div>'
    hs += '</boody></html>'
    return hs

@app.route('/controls')
def www_controls():
    return render_template('controls.html')

@app.route('/dashboard')
def www_dashboard():
    return render_template('index.html')

@app.route('/pump5')
def www_pump5():
    command_fifo.sendcommand('water_for 300')
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
