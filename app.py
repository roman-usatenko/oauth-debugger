import json
import config
import urllib.parse
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for("authorize", server=config.get_first_server_name()))


@app.route('/authorize/<server>', methods=['GET'])
def authorize(server):
    srv = config.get_server_config(server)
    params = request.args
    if len(params) == 0:
        params = srv["params"].copy()
        params.pop("client_secret")
        return redirect(request.url + "?" + urllib.parse.urlencode(params))
    servers = config.CONFIG["servers"].keys()
    metadata_url = srv["metadata"]
    authorize_url = srv["urls"]["authorization_endpoint"] + "?" + urllib.parse.urlencode(params)
    return render_template('authorize.html', 
        servers=servers, 
        server=server, 
        metadata_url=metadata_url, 
        authorize_url=authorize_url, 
        params=params)

