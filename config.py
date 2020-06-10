import json
import requests
import os

CONFIG_FILE = os.path.expanduser('~') + '/.oad/config.json'
if not os.path.exists(CONFIG_FILE):
    CONFIG_FILE = "config.json"

print(" * Using config file: " + CONFIG_FILE)

with open(CONFIG_FILE, "r") as config:
    CONFIG = json.load(config)


def get_server_config(server):
    cfg = CONFIG["servers"][server]
    if "metadata" not in cfg:
        try:
            cfg["metadata"] = requests.get(
                cfg["metadata_url"], verify=False).json()
        except:
            pass
    return cfg


def get_defaults(cfg, endpoint):
    param_names = cfg[endpoint+"_defaults"]
    result = {}
    for p in param_names:
        result[p] = cfg["params"][p]
    return result


def get_servers():
    return CONFIG["servers"].keys()


if __name__ == "__main__":
    print(get_server_config("AAD"))
