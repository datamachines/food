#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
from os.path import expanduser
import json
import yaml

config_file = expanduser("~") + '/.food/truck-chaser-config'
config = yaml.safe_load(open(config_file))

foodtrucks = [{
                'url':'http://foodtruckfiesta.com/astro-doughnuts-fried-chicken-food-truck/',
                'name':'Astro Doughnuts'
            }]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def slacksend(message):
    slack_payload = {
        "text": message,
        "channel": config['channel'],
        "icon_emoji": config['emoji'],
        "username": config['username']
        }

    print "sending to slack...", slack_payload
    r = requests.post(config['slack_webhook_url'],
        data = json.dumps(slack_payload))
    print "slack response:", r.text


for truck in foodtrucks:
    response = requests.get(truck['url'], headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        location = str(soup.find("div", {"id": "truck_location_text"}))
        if "Arlington" in location:
            message = truck['name'] + " is in Arlington!"
            slacksend(message)
        else:
          print "no joy"
    else:
        print "Unable to fetch " + truck['name']
