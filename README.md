# Home Assistant DoorBird Proxy

## Introduction

This simple Flask app translates the DoorBird API calls to appropriate calls for Home Assistant. 
Basically it translates the weird GET requests to POST requests.

## Setting up Home Assistant

Create two binary sensors within Home Assistant, eg.:

```yaml
binary_sensor:
  - platform: template
    sensors:
      doorbell:
        friendly_name: Doorbell
        device_class: sound
        value_template: 'off'
        entity_id: foo.bar
      frontdoor_motion:
        friendly_name: Front Door Motion
        device_class: motion
        value_template: 'off'
        entity_id: foo.bar
      frontdoor_open:
        friendly_name: Front Door Open
        device_class: opening
        value_template: 'off'
        entity_id: foo.bar
```

## Run the proxy

The easiest way to fire up the proxy is by Docker, the image is based on uWSGI and Nginx. 
But, running it without Docker should also work.

```bash
docker run -d -p 5123:80 \
  -e HA_API_URL=http://${homeassistant.url}:8123/api \
  -e HA_DOORBELL_ENTITY=binary_sensor.doorbell \
  -e HA_FRONTDOORMOTION_ENTITY=binary_sensor.frontdoor_motion \
  -e HA_FRONTDOOROPEN_ENTITY=binary_sensor.frontdoor_open \
  basschipper/homeassistant-doorbird-proxy:latest
```

##### Where:
- ${homeassistant.url} = your Home Assistant URL or IP

## Setup DoorBird API

Configure the doorbell event:
```bash
curl -k 'https://${doorbird.url}/bha-api/notification.cgi?url=http%3A%2F%2F${homeassistant.url}%3A5123%2Fdoorbell&event=doorbell&subscribe=1&http-user=${doorbird.user}&http-password=${doorbird.password}'
```
Configure the motionsensor event:
```bash
curl -k 'https://${doorbird.url}/bha-api/notification.cgi?url=http%3A%2F%2F${homeassistant.url}%3A5123%2Ffrontdoormotion&event=motionsensor&subscribe=1&http-user=${doorbird.user}&http-password=${doorbird.password}'
```
Configure the dooropen event:
```bash
curl -k 'https://${doorbird.url}/bha-api/notification.cgi?url=http%3A%2F%2F${homeassistant.url}%3A5123%2Ffrontdooropen&event=dooropen&subscribe=1&http-user=${doorbird.user}&http-password=${doorbird.password}'
```
##### Where:
- ${homeassistant.url} = your Home Assistant URL or IP (if running the proxy on another box, use that ip for the curl entrys instead)
- ${doorbird.url} = your DoorBird URL or IP
- ${doorbird.user} = your DoorBird Username
- ${doorbird.password} = your DoorBird Password

## More info

- [DoorBird API](http://www.doorbird.com/api/)
- [Home Assistant API](https://home-assistant.io/developers/rest_api/)
- [uwsgi-nginx-flask](https://github.com/tiangolo/uwsgi-nginx-flask-docker)
- [Python](https://www.python.org/)
- [Flask](http://flask.pocoo.org/)
