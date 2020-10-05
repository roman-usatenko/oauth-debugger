import json
import requests
import os

SERVER = os.environ['OAD_SERVER']
CONFIG_FILE = '.oad/' + SERVER + ".json"
CONFIG_FILE_PATH = os.path.expanduser('~') + '/' + CONFIG_FILE

if not os.path.exists(CONFIG_FILE_PATH):
    CONFIG_FILE_PATH = "./" + CONFIG_FILE

if not os.path.exists(CONFIG_FILE_PATH):
    raise Exception("Configuraion file " + CONFIG_FILE + " cannot be found")

print(" * Using config file: " + CONFIG_FILE_PATH)

with open(CONFIG_FILE_PATH, "r") as config:
    CONFIG = json.load(config)
    CONFIG["metadata"] = requests.get(
        CONFIG["metadata_url"], verify=False).json()


def get_defaults(endpoint):
    param_names = CONFIG[endpoint+"_defaults"]
    result = {}
    for p in param_names:
        result[p] = CONFIG["params"][p]
    return result
