#!/usr/local/bin/python3

# Example python code to access the openVuln API
# Based on contributions from Ryan Ruckley
# Requirements:
#  - Python version 3
#  - oauth2 - sudo pip3 install oauth2
#  - oauth2 - sudo pip3 install request

import oauth2 as oauth
import json
# import urllib.request # python3 version
import urllib2
from pprint import pprint


print('Connecting to Cisco...')

consumer = oauth.Consumer(key="ra4gcdmq64numrums2ps4khx",
                          secret="ZdccKYYpQHPKPfn6xBuC2Vvm")

request_token_url = "https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id=ra4gcdmq64numrums2ps4khx&client_secret=ZdccKYYpQHPKPfn6xBuC2Vvm"

client = oauth.Client(consumer)

resp, content = client.request(request_token_url, "POST")

print(content)

j = json.loads(content.decode('utf-8'))

print('Access Token Retrieved...')
print(j['access_token'])

# Replace the Request URL below with the openVuln REST API resource you
# would like to access.
# The available resources are documented at:
# https://developer.cisco.com/site/PSIRT/get-started/getting-started.gsp

req = urllib2.Request('https://api.cisco.com/security/advisories/oval/latest/100')
req.add_header('Accept', 'application/json')
req.add_header('Authorization', 'Bearer '+j['access_token'])
resp = urllib2.urlopen(req)
adv = resp.read()

advdata = json.loads(adv.decode('utf-8'))

for advisory in advdata['advisories']:
    pprint(advisory)
