import json
import config
import urllib.parse
import utilz
import requests
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)


def get_server():
    server = config.get_first_server_name()
    if "server" in request.cookies:
        srv = request.cookies.get("server")
        if srv in config.get_servers():
            server = srv
    return server


@app.route('/')
def index():
    resp = redirect(url_for("authorize"))
    resp.set_cookie("server", get_server())
    return resp


@app.route('/authorize/', methods=['GET'])
def authorize():
    server = get_server()
    srv = config.get_server_config(server)
    servers = config.get_servers()
    metadata_url = srv["metadata"]

    params = request.args
    if len(params) == 0:
        params = config.get_defaults(server, "authorize")
        return redirect(request.url + "?" + urllib.parse.urlencode(params))
    authorize_url = srv["urls"]["authorization_endpoint"] + \
        "?" + urllib.parse.urlencode(params)
    return render_template('authorize.html',
                           servers=servers,
                           server=server,
                           metadata_url=metadata_url,
                           authorize_url=authorize_url,
                           params=params)


@app.route('/token/', methods=['GET'])
def token_get():
    server = get_server()
    srv = config.get_server_config(server)
    servers = config.get_servers()
    metadata_url = srv["metadata"]

    params = request.args
    if len(params) == 0:
        params = config.get_defaults(server, "token")
        return redirect(request.url + "?" + urllib.parse.urlencode(params))

    return render_template('token.html',
                           servers=servers,
                           server=server,
                           metadata_url=metadata_url,
                           params=params)


@app.route('/token', methods=['POST'])
def token_post():
    server = get_server()
    srv = config.get_server_config(server)
    servers = config.get_servers()
    metadata_url = srv["metadata"]

    token_url = srv["urls"]["token_endpoint"]
    data = request.form.to_dict()
    data.pop("_newParam")
    data.pop("_newParamValue")
    resp = requests.post(token_url, data, verify=False)
    status = str(resp.status_code) + " / " + str(resp.reason)
    text = resp.text
    headers = resp.headers
    params = {}
    try:
        params = resp.json()
    except:
        params = {}
    params = utilz.process_params(params)
    return render_template('token_response.html',
                           servers=servers,
                           server=server,
                           metadata_url=metadata_url,
                           status=status,
                           headers=headers,
                           text=text,
                           params=params)


@app.route('/reply', methods=['GET'])
def reply_get():
    server = get_server()
    srv = config.get_server_config(server)
    servers = config.get_servers()
    metadata_url = srv["metadata"]

    params = utilz.process_params(request.args)
    response_mode = "URL fragment" if len(
        params) == 0 else "query string parameters"
    return render_template('authorize_response.html',
                           servers=servers,
                           server=server,
                           metadata_url=metadata_url,
                           response_mode=response_mode,
                           params=params)


@app.route('/reply-fragment/', methods=['GET'])
def reply_fragment():
    server = get_server()
    srv = config.get_server_config(server)
    servers = config.get_servers()
    metadata_url = srv["metadata"]

    params = utilz.process_params(request.args)
    servers = config.get_servers()
    response_mode = "URL fragment"
    return render_template('authorize_response.html',
                           servers=servers,
                           server=server,
                           metadata_url=metadata_url,
                           response_mode=response_mode,
                           params=params)


@app.route('/reply-post/', methods=['GET'])
def reply_post():
    server = get_server()
    srv = config.get_server_config(server)
    servers = config.get_servers()
    metadata_url = srv["metadata"]

    params = utilz.process_params(request.args)
    servers = config.get_servers()
    response_mode = "form post"
    return render_template('authorize_response.html',
                           servers=servers,
                           server=server,
                           metadata_url=metadata_url,
                           response_mode=response_mode,
                           params=params)


@app.route('/reply', methods=['POST'])
def reply1():
    return redirect(url_for("reply_post") + "?" + urllib.parse.urlencode(request.form))


@app.route('/redeem', methods=['GET'])
def redeem():
    server = get_server()
    params = config.get_defaults(server, "token")
    params.update(request.args)
    if "code" in request.args:
        params["grant_type"] = "authorization_code"
    if "refresh_token" in request.args:
        params["grant_type"] = "refresh_token"

    return redirect(url_for("token_get") + "?" + urllib.parse.urlencode(params))
