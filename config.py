import json
import urllib.request
import os

CONFIG_FILE = os.path.expanduser('~') + '/.oad/config.json'
if not os.path.exists(CONFIG_FILE):
    CONFIG_FILE = "config.json"

print(" * Using config file: " +CONFIG_FILE)

with open(CONFIG_FILE, "r") as config:
    CONFIG = json.load(config)


def get_first_server_name():
    for k in CONFIG["servers"]:
        return k


def get_server_config(server):
    cfg = CONFIG["servers"][server]
    if "urls" not in cfg:
        with urllib.request.urlopen(cfg["metadata"]) as url:
            metadata = json.loads(url.read().decode())
        urls = {}
        urls["authorization_endpoint"] = metadata["authorization_endpoint"]
        urls["token_endpoint"] = metadata["token_endpoint"]
        urls["jwks_uri"] = metadata["jwks_uri"]
        urls["end_session_endpoint"] = metadata["end_session_endpoint"]
        cfg["urls"] = urls
    return cfg


def get_defaults(server, endpoint):
    cfg = get_server_config(server)
    param_names = cfg[endpoint+"_defaults"]
    result = {}
    for p in param_names:
        result[p] = cfg["params"][p]
    return result


def get_servers():
    return CONFIG["servers"].keys()


if __name__ == "__main__":
    print(get_server_config("AAD"))
