#!/usr/bin/env python3

import argparse
import json
import pprint
import os
import settings
import argschema
import requests
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
@app.route("/render/<server>/<owner>/<project>/<stack>/",
           defaults={'channel': None})
@app.route("/render/<server>/<owner>/<project>/<stack>/<channel>/")
def render(server, owner, project, stack, channel):
    config = settings.get_settings(request.args).args

    if config['render']['all_channels']:
        # Check for all available channels
        # http://localhost:8080/render-ws/v1/owner/E/project/C/stack/S2_RoughAligned
        if config['render']['alt_render']:
            apiserver = config['render']['alt_render']
        else:
            apiserver = server
        stack_info_url = "{0}://{1}/render-ws/v1/owner/{2}/project/{3}/stack/{4}".format(
            config['render']['protocol'], apiserver, owner, project, stack)
        stack_info = requests.get(stack_info_url).json()

        params = {'layers' : {}}
        if len(stack_info["stats"]["channelNames"]) > 0:
            for channel in stack_info["stats"]["channelNames"]:
                render_params = [owner, project, stack]
                if channel:
                    render_params.append(channel)
                
                render_source = "render://{0}://{1}/{2}?encoding={3}".format(
                config['render']['protocol'], server,
                '/'.join(render_params), config['render']['encoding'])


                layer = {'type': 'image', 'source': render_source}
                layer = argschema.utils.smart_merge(layer,
                        config['neuroglancer']['layer_options'])
                params['layers'][channel] = layer
            params = argschema.utils.smart_merge(params, config['neuroglancer']['options'])
            params_json = json.dumps(params, separators=(',', ':'))
            new_url = "{0}/#!{1}".format(config['neuroglancer']['base_url'],
                                    params_json)
            new_url = new_url.replace('"', "'")
            return redirect(new_url, code=303)
        else:
            pass # Default to use the regular code path (below) when there are no channels

    render_params = [ owner, project, stack]
    if channel:
        render_params.append(channel)
    
    render_source = "render://{0}://{1}/{2}?encoding={3}".format(
        config['render']['protocol'], server,
        '/'.join(render_params), config['render']['encoding'])

    params = {}
    layer = {'type': 'image', 'source': render_source}
    layer = argschema.utils.smart_merge(layer,
                                        config['neuroglancer']
                                            ['layer_options'])
    params['layers'] = {stack: layer}
    params = argschema.utils.smart_merge(params,
                                        config['neuroglancer']['options'])
    params_json = json.dumps(params, separators=(',', ':'))
    new_url = "{0}/#!{1}".format(config['neuroglancer']['base_url'],
                                params_json)
    new_url = new_url.replace('"', "'")

    return redirect(new_url, code=303)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store", type=int, default=5000)
    parser.add_argument("--host", action="store", type=str, default="0.0.0.0")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
