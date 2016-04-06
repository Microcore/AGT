# coding: utf-8
from __future__ import unicode_literals, print_function

from flask import Flask, jsonify, request
from gevent.wsgi import WSGIServer

from vol import VolumeController

app = Flask('AGT daemon')
app.volctrl = VolumeController()
DEFAULT_CHANNEL = app.volctrl.get_volume_channels()[0]


@app.route('/volume/', defaults={'channel': DEFAULT_CHANNEL}, methods=('GET',))
@app.route('/volume/<channel>', methods=('GET', ))
def api_get_volume(channel):
    return jsonify({
        'value': app.volctrl.get_volume(channel),
    })


@app.route('/volume/', defaults={'channel': DEFAULT_CHANNEL}, methods=('GET',))
@app.route('/volume/<channel>', methods=('POST', ))
def api_set_volume(channel):
    app.volctrl.set_volume(request.form['value'])


@app.route('/volume/step/', defaults={'channel': DEFAULT_CHANNEL}, methods=('GET',))
@app.route('/volume/step/<channel>', methods=('GET', ))
def api_get_step(channel):
    return jsonify({
        'value': app.volctrl.get_volume_step(channel),
    })


@app.route('/volume/channels', methods=('GET', ))
def api_get_channels():
    return jsonify({
        'channels': app.volctrl.get_volume_channels(),
    })


@app.route('/volume/range/', defaults={'channel': DEFAULT_CHANNEL}, methods=('GET',))
@app.route('/volume/range/<channel>', methods=('GET', ))
def api_get_range(channel):
    minimum, maximum = app.volctrl.get_volume_range(channel)
    return jsonify({
        'minimum': minimum,
        'maximum': maximum,
    })


def start():
    WSGIServer(('', 2016), app).serve_forever()


def debug():
    app.debug = True
    app.run('', 2016)


if __name__ == '__main__':
    start()
