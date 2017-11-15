import os
import requests
import json
import time

from flask import Flask
app = Flask(__name__)

ha_api_url = os.getenv('HA_API_URL', 'http://localhost:8123/api')
ha_api_password = os.getenv('HA_API_PASSWORD', None)
ha_doorbell_entity = os.getenv('HA_DOORBELL_ENTITY', 'binary_sensor.doorbell')
ha_frontdoormotion_entity = os.getenv('HA_FRONTDOORMOTION_ENTITY', 'binary_sensor.frontdoor_motion')
ha_frontdooropen_entity = os.getenv('HA_FRONTDOOROPEN_ENTITY', 'binary_sensor.frontdoor_open')


@app.route("/")
def default():
    return "OK"


@app.route("/doorbell")
def doorbell():
    return trigger_ha_entity(ha_doorbell_entity)


@app.route("/frontdoormotion")
def frontdoormotion():
    return trigger_ha_entity(ha_frontdoormotion_entity)


@app.route("/frontdooropen")
def frontdooropen():
    return trigger_ha_entity(ha_frontdooropen_entity)


def trigger_ha_entity(name):
    client = HomeAssistantApiClient(ha_api_url, ha_api_password)

    try:
        entity = client.get_entity(name)
    except HomeAssistantApiException as e:
        return e.message, e.status_code

    entity = {'state': 'on', 'attributes': entity['attributes']}
    try:
        client.update_entity(name, entity)
    except HomeAssistantApiException as e:
        return e.message, e.status_code

    time.sleep(1)

    entity = {'state': 'off', 'attributes': entity['attributes']}
    try:
        client.update_entity(name, entity)
    except HomeAssistantApiException as e:
        return e.message, e.status_code

    return "OK"


class HomeAssistantApiClient(object):
    def __init__(self, base_url, api_password=None):
        self.base_url = base_url
        self.headers = {'content-type': 'application/json'}
        if api_password is not None:
            self.headers.update({'X-HA-Access': api_password})

    def get_entity(self, name):
        url = '{}/states/{}'.format(self.base_url, name)
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise HomeAssistantApiException(
                response.status_code, 'Error getting entity from Home Assistant with: {0}'.format(response.content))

        return response.json()

    def update_entity(self, name, data):
        url = '{}/states/{}'.format(self.base_url, name)
        response = requests.post(url, headers=self.headers, data=json.dumps(data))

        if response.status_code != 200:
            raise HomeAssistantApiException(
                response.status_code, 'Error updating entity at Home Assistant with: {0}'.format(response.content))

        return response.json()


class HomeAssistantApiException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
