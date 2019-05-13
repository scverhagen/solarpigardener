#!/usr/bin/python3
import os
from flask import Flask, request, send_file
app = Flask(__name__)

import simple_html as html

thisfilepath = os.path.dirname(__file__)

@app.route('/')
def www_root():
    hs = html.html_start()
    hs += html.readfile('navbar')
    hs += '<div class="jumbotron">'
    hs += '<h3>Dashboard</h3>'
    hs += '</div>'
    hs += '</boody></html>'
    return hs
    
@app.route('/dashboard')
def wwww_dashboard():
    return www_root()

@app.route('/systeminfo')
def www_systeminfo():
    hs = html.html_start()
    hs += html.readfile('navbar')
    hs += '<div class="jumbotron">'
    hs += '<h3>System Info</h3>'
    hs += '</div>'
    hs += '</boody></html>'
    return hs

@app.route('/settings')
def www_settings():
    hs = html.html_start()
    hs += html.readfile('navbar')
    hs += '<div class="jumbotron">'
    hs += '<h3>Settings</h3>'
    hs += '</div>'
    hs += '</boody></html>'
    return hs

@app.route('/getimage')
def www_getimg():
    img = request.args.get('image')
    return(html.getimage(img))

@app.route('/favicon.ico')
def www_favicon():
    return(html.getimage('logo.png'))

#needs to be at end of file:
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088, threaded=True)
