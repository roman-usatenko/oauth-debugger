import json
import urllib.request

with open("config.json", "r") as config:
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

if __name__ == "__main__":
    print(get_server_config("AAD"))