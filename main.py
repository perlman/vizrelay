#!/usr/bin/env python3

import json
import pprint
import os
import settings
import sys

from flask import Flask, request, redirect

app = Flask(__name__)
app.config['RELAY_CONFIG_FILE'] = os.environ.get(
    "RELAY_CONFIG_FILE",
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
)
app.config['RELAY_CONFIG_JSON'] = os.environ.get(
    "RELAY_CONFIG_JSON",
    "{}")

@app.before_first_request
def setup():
    if 'RELAY_CONFIG_FILE' in app.config:
        settings.add_defaults(json.load(open(app.config['RELAY_CONFIG_FILE'])))
    if 'RELAY_CONFIG_JSON' in app.config:
        settings.add_defaults(json.loads(app.config['RELAY_CONFIG_JSON']))


@app.route("/")
def main():
    mod = settings.get_settings(request.args)
    result = "<html><head></head><body>"
    result += "<h2>Current settings</h2>"
    result += "<pre>" + pprint.PrettyPrinter(indent=4).pformat(
        mod.args) + "</pre>"
    result += "</body>"
    return result


# Sample URL http://ibs-forrestc-ux1:8002/render/ibs-forrestc-ux1.corp.alleninstitute.org/Forrest/H16_03_005_HSV_HEF1AG65_R2An15dTom/ACQGephyrin/
@app.route("/render/<server>/<owner>/<project>/<stack>/", defaults={'channel': None})
@app.route("/render/<server>/<owner>/<project>/<stack>/<channel>/")
def render(server, owner, project, stack, channel):
    config = settings.get_settings(request.args).args

    render_params = [owner, project, stack]
    if channel:
        render_params.append(channel)
        
    render_source = "render://{0}://{1}/{2}".format(
        config['render']['protocol'], server,
        '/'.join(render_params))

    params = {}
    layer = {'type': 'image', 'source': render_source}
    params['layers'] = {stack: layer}
    params['blend'] = config['neuroglancer']['blend']

    new_url = "{0}/#!{1}".format(config['neuroglancer']['base_url'],
        json.dumps(params, separators=(',', ':')).replace('"', "'"))

    return redirect(new_url, code=303)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
