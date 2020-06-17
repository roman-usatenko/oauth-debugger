import json
import base64
import html

def process_params(params):
    result = {}
    for k,v in params.items():
        result[k] = jwt_decode(v)
    return result

def jwt_decode(val):
    val=str(val)
    try:
        jwt = val.split('.')
        protection = json.loads(base64.b64decode(jwt[0]  + "===").decode('utf-8'))
        payload = json.loads(base64.b64decode(jwt[1] + "===").decode('utf-8'))
        return (json.dumps((protection, payload),indent=4),val)
    except:
        return (html.escape(val),val)