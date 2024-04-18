#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import datetime
import time
from bs4 import BeautifulSoup

CACHE_FILE="not/telex.cache"
CODE='<my-code>'

foxpostContent = []
url = f"https://foxpost.hu/csomagkovetes/?code={CODE}"
headers = {'accept': 'text/html'}

try:
    response = requests.get(url, headers=headers, timeout=(3.05, 27))
    soup = BeautifulSoup(response.text, 'html.parser')
except Exception as e:
    print("Couldn't parse response. 💀")
    print(e)
    exit(0)

first = True

for litag in soup.find_all('li', attrs={'class' : 'parcel-status-items__list-item'}):
    for dateSpan in litag.find_all('span', attrs={'class' : 'parcel-status-items__list-item-date'}):
        dateText = dateSpan.text
    for textSpan in litag.find_all('span', attrs={'class' : 'parcel-status-items__list-item-text'}):
        spanText = textSpan.text.split('\n')
    if first:
        first = False
        foxpostContent.append("%s" % (f"🦊 {spanText[1]}"))
        foxpostContent.append("%s" % (f"--"))
        foxpostContent.append("%s" % (f"Link|href={url}"))
        foxpostContent.append("%s" % (f"--"))
    foxpostContent.append("%s" % (f"{dateText} :: {spanText[1]}"))
    
content = '\n'.join(foxpostContent)
print(content)
