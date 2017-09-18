import os
import requests
import json
import time

from flask import Flask
app = Flask(__name__)

ha_api_url = os.getenv('HA_API_URL', 'http://localhost:8123/api')
ha_doorbell_entity = os.getenv('HA_DOORBELL_ENTITY', 'binary_sensor.doorbell')
ha_frontdoormotion_entity = os.getenv('HA_FRONTDOORMOTION_ENTITY', 'binary_sensor.frontdoor_motion')
ha_frontdooropen_entity = os.getenv('HA_FRONTDOOROPEN_ENTITY', 'binary_sensor.frontdoor_open')

@app.route("/")
def default():
    return "OK"

@app.route("/doorbell")
def doorbell():
    headers = {'content-type': 'application/json'}
    url = '{}/states/{}'.format(ha_api_url, ha_doorbell_entity)

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return res.content, res.status_code

    entity = res.json()

    data = {'state': 'on', 'attributes': entity['attributes']}
    res  = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code != 200:
        return res.content, res.status_code

    time.sleep(1)

    data = {'state': 'off', 'attributes': entity['attributes']}
    res  = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code != 200:
        return res.content, res.status_code

    return "OK", res.status_code

@app.route("/frontdoormotion")
def frontdoormotion():
    headers = {'content-type': 'application/json'}
    url = '{}/states/{}'.format(ha_api_url, ha_frontdoormotion_entity)

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return res.content, res.status_code

    entity = res.json()

    data = {'state': 'on', 'attributes': entity['attributes']}
    res  = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code != 200:
        return res.content, res.status_code

    time.sleep(1)

    data = {'state': 'off', 'attributes': entity['attributes']}
    res  = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code != 200:
        return res.content, res.status_code

    return "OK", res.status_code

@app.route("/frontdooropen")
def frontdooropen():
    headers = {'content-type': 'application/json'}
    url = '{}/states/{}'.format(ha_api_url, ha_frontdooropen_entity)

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return res.content, res.status_code

    entity = res.json()

    data = {'state': 'on', 'attributes': entity['attributes']}
    res  = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code != 200:
        return res.content, res.status_code

    time.sleep(1)

    data = {'state': 'off', 'attributes': entity['attributes']}
    res  = requests.post(url, headers=headers, data=json.dumps(data))
    if res.status_code != 200:
        return res.content, res.status_code

    return "OK", res.status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
