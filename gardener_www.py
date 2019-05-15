#!/usr/bin/python3
import os
from flask import Flask, request, send_file
app = Flask(__name__)

import simple_html as html
import gardener_fifo

thisfilepath = os.path.dirname(__file__)
status_fifo = gardener_fifo.status_fifo()
command_fifo = gardener_fifo.command_fifo()

@app.route('/dashboard')
def wwww_dashboard():
    status_dict = status_fifo.getstatusdict()
    
    hs = html.html_start()
    hs += html.readfile('navbar')
    hs += '<div class="jumbotron">'
    hs += '<h3>Service</h3>'
    hs += """
    <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-center">
        """
    hs += 'Uptime (in seconds) <span class="badge badge-primary badge-pill">' + str(status_dict['uptime']) + '</span>'
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
    hs += 'Battery Voltage<span class="badge badge-primary badge-pill">' + str(status_dict['bat_voltage']) + '</span>'
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
    hs += 'Soil Moisture Reading<span class="badge badge-primary badge-pill">' + str(status_dict['moisture_reading']) + '</span>'
    hs += """
        </li>
    </ul>
    """

    hs += '</div>'
    hs += '</boody></html>'
    return hs

@app.route('/controls')
def www_settings():
    hs = html.html_start()
    hs += html.readfile('navbar')
    hs += '<div class="jumbotron">'
    hs += '<h3>Controls</h3>'
    hs += """
    <button class="btn btn-primary" type="submit" onclick="window.location.href='/pump5'">Pump water for 5 mins</button>
    """
    hs += '</div>'
    hs += '</boody></html>'
    return hs

@app.route('/pump5')
def www_pump5():
    hs = html.html_start()
    hs += html.readfile('navbar')
    hs += '<div class="jumbotron">'
    hs += 'Pumping water for 5 minutes...'
    hs += '</div>'
    hs += '</boody></html>'
    command_fifo.sendcommand('water_for 300')
    return hs

@app.route('/getimage')
def www_getimg():
    img = request.args.get('image')
    return(html.getimage(img))

@app.route('/favicon.ico')
def www_favicon():
    return(html.getimage('logo.png'))

@app.route('/')
def www_root():
    return wwww_dashboard()

#needs to be at end of file:
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088, threaded=True)
