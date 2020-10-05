import json
import sys
import config
import urllib.parse
import utilz
import requests
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

def get_server():
    return (config.SERVER, config.CONFIG)


@app.route('/')
def index():
    resp = redirect(url_for("authorize"))
    return resp


@app.route('/authorize/', methods=['GET'])
def authorize():
    server = get_server()
    params = request.args
    if len(params) == 0:
        params = config.get_defaults("authorize")
        return redirect(request.url + "?" + urllib.parse.urlencode(params))
    authorize_url = server[1]["metadata"]["authorization_endpoint"] + \
        "?" + urllib.parse.urlencode(params)
    return render_template('authorize.html',
                           server=server,
                           authorize_url=authorize_url,
                           params=params)


@app.route('/token/', methods=['GET'])
def token_get():
    server = get_server()
    params = request.args
    if len(params) == 0:
        params = config.get_defaults("token")
        return redirect(request.url + "?" + urllib.parse.urlencode(params))

    return render_template('token.html',
                           server=server,
                           params=params)


@app.route('/token', methods=['POST'])
def token_post():
    server = get_server()
    token_url = server[1]["metadata"]["token_endpoint"]
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
                           server=server,
                           status=status,
                           headers=headers,
                           text=text,
                           params=params)


@app.route('/reply', methods=['GET'])
def reply_get():
    server = get_server()
    params = utilz.process_params(request.args)
    response_mode = "URL fragment" if len(
        params) == 0 else "query string parameters"
    return render_template('authorize_response.html',
                           server=server,
                           response_mode=response_mode,
                           params=params)


@app.route('/reply-fragment/', methods=['GET'])
def reply_fragment():
    server = get_server()
    params = utilz.process_params(request.args)
    response_mode = "URL fragment"
    return render_template('authorize_response.html',
                           server=server,
                           response_mode=response_mode,
                           params=params)


@app.route('/reply-post/', methods=['GET'])
def reply_post():
    server = get_server()
    params = utilz.process_params(request.args)
    response_mode = "form post"
    return render_template('authorize_response.html',
                           server=server,
                           response_mode=response_mode,
                           params=params)


@app.route('/reply', methods=['POST'])
def reply1():
    return redirect(url_for("reply_post") + "?" + urllib.parse.urlencode(request.form))


@app.route('/redeem', methods=['GET'])
def redeem():
    server = get_server()
    params = config.get_defaults("token")
    params.update(request.args)
    if "code" in request.args:
        params["grant_type"] = "authorization_code"
    if "refresh_token" in request.args:
        params["grant_type"] = "refresh_token"

    return redirect(url_for("token_get") + "?" + urllib.parse.urlencode(params))
