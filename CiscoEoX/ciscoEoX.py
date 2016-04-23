#!/usr/local/bin/python3

# Example python code to access the Cisco Product EoX API
# Requirements:
#  - Python version 2.7.11
#  - oauth2 - sudo pip install oauth2
#  - urillib2 - sudo pip install urillib2

import oauth2 as oauth
import json
import urllib
import urllib2
from pprint import pprint

data = {}
data['pageIndex'] = '1'
data['productIDs'] = 'WS-C3560X-24PS-S'
data['responseencoding'] = 'json'
url_values = urllib.urlencode(data)
print url_values  # The order may differ.
eox_url = "https://apx.cisco.com/devlab/apicem/eox/"
eox_version = 'POC'


print('Connecting to Cisco...')

consumer = oauth.Consumer(key="4c806ffe4a1045ceafe9c6c0143ddea2",
                          secret="bc1d4d4a6bd84a7896D1C3C8E3DF2419")

request_token_url = "https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id=4c806ffe4a1045ceafe9c6c0143ddea2&client_secret=bc1d4d4a6bd84a7896D1C3C8E3DF2419"

client = oauth.Client(consumer)

resp, content = client.request(request_token_url, "POST")

print(content)

j = json.loads(content.decode('utf-8'))

print('Access Token Retrieved...')
print(j['access_token'])

req = urllib2.Request(eox_url + eox_version + "/EOXByProductID" + "?" + url_values)
#req.add_header('Accept', 'application/json')
req.add_header('Authorization', j['access_token'])
resp = urllib2.urlopen(req)
adv = resp.read()

eoxdata = json.loads(eox.decode('utf-8'))

for productID in eoxdata['EOXRecord']:
    pprint(productID)
