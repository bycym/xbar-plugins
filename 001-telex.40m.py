#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import datetime
import time


print("📮")
print("---")
print("ʇ legfontosabb | href=https://telex.hu/legfontosabb")
print("Refresh... | refresh=true")
print("---")

CACHE_FILE="not/telex.cache"


def fallback():
  with open(CACHE_FILE, "r") as f:
    stored_feed = f.read()
  if(len(stored_feed) > 0):
    print(stored_feed)
  else:
    print ("No cache...")  

telexFeed = []
url = 'https://telex.hu/rss'
headers = {'accept': 'application/xml;q=0.9, */*;q=0.8'}
# The timeout value will be applied to both the connect and the read timeouts. Specify a tuple if you would like to set the values separately:
try:
    response = requests.get(url, headers=headers, timeout=(3.05, 27))
    telexXML = ET.fromstring(response.text)
except:
    print("Couldn't parse response. 💀")
    fallback()
    exit(0)

for x in telexXML.iter('item'):
    # Tue, 26 Apr 2022 08:14:10 +0200
    pubDate = x.find('pubDate').text
    feedTime = datetime.datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S +%f').strftime('%a %H:%M')
    # pubDate = "zolo"
    title = x.find('title').text.replace('\n', ' ').replace('\r', '')
    category = x.find('category').text.replace('\n', ' ').replace('\r', '')
    description = x.find('description').text.replace('\n', ' ').replace('\r', '')
    link = x.find('link').text
    telexFeed.append("%s" % (f"{feedTime} ~ {category} :: {title}"))
    telexFeed.append("%s" % (f"--{description} | href={link}"))
content = '\n'.join(telexFeed)
print(content)
# print (response.text)

if not telexXML:
    print("connection error")
    fallback()

with open(CACHE_FILE, "w+") as f:
    f.write(content)
    f.write("\n---\n")
    f.write("cached\n")
    f.write(time.ctime())
    f.close()
