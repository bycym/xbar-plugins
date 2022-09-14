#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import datetime


print("📮")
print("---")
print("Refresh... | refresh=true")
print("---")

url = 'https://telex.hu/rss'
headers = {'accept': 'application/xml;q=0.9, */*;q=0.8'}
# The timeout value will be applied to both the connect and the read timeouts. Specify a tuple if you would like to set the values separately:
try:
    response = requests.get(url, headers=headers, timeout=(3.05, 27))
    telexXML = ET.fromstring(response.text)
except:
    print("Couldn't parse response. 💀")
    exit(0)


for x in telexXML.iter('item'):
    # Tue, 26 Apr 2022 08:14:10 +0200
    pubDate = x.find('pubDate').text
    time = datetime.datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S +%f').strftime('%a %H:%M')
    title = x.find('title').text.replace('\n', ' ').replace('\r', '')
    link = x.find('link').text
    print(f"{time} :: {title} | href={link}")
