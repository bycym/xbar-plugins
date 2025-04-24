#!/usr/bin/python3
# -*- coding: utf-8 -*-


# May need to pip(3) install pillow
# May need to install certificates: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
import base64
import urllib.request
from PIL import Image
import io
from io import BytesIO

import xml.etree.ElementTree as ET
import datetime
import time
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

print('🔭')
print('---')
print('Refresh... | refresh=true')
img_prefix = "RccW"
CACHE_FILE="not/radar.cache"
radarFeed = []
headers = {'accept': 'application/xml;q=0.9, */*;q=0.8'}
timezone_name = "Europe/Budapest"


def is_summer_time(timezone) -> bool:
    timezone = ZoneInfo(timezone)
    now = datetime.now(timezone)

    if now.utcoffset().total_seconds() == 7200:  # UTC+2
        return True
    else:  # UTC+1
        return False

def fallback():
    with open(CACHE_FILE, "r") as f:
        stored_feed = f.read()
    if(len(stored_feed) > 0):
        print(stored_feed)
    else:
        print ("No cache...")

def radar_picture(rounded_time)-> str:
    # Format the time into a filename
    # example: https://www.met.hu/img/RccW/RccW20250321_1305.jpg
    url = "https://www.met.hu/img/RccW/"
    ext = ".jpg"
    filename = rounded_time.strftime("%Y%m%d_%H%M")
    filename = f"{url}{img_prefix}{filename}{ext}"

    # get the picture
    image_path = io.BytesIO(urllib.request.urlopen(filename).read())
    pillow_image = Image.open(image_path)
    maxsize = (720, 720)

    pillow_image.thumbnail(maxsize)
    buff = BytesIO()
    pillow_image.save(buff, format="JPEG")
    encoded_string = base64.b64encode(buff.getvalue())
    return f"| href=https://www.met.hu/idojaras/aktualis_idojaras/radar/ image={str(encoded_string)[2:][:-1]}"

def weather_picture(rounded_time)->str:
    # example: "https://www.met.hu/completed/fhwa/fhwaT20250321_1045_2114+_1790_4710.png"
    # location veszprém
    url = "https://www.met.hu/completed/fhwa/"
    ext = "_0905_2110+_1790_4710.png"
    # Format the time into a filename
    filename = rounded_time.strftime("%Y%m%d_%H%M")
    filename = f"{url}{img_prefix}{filename}{ext}"

    # get the picture
    image_path = io.BytesIO(urllib.request.urlopen(filename).read())
    pillow_image = Image.open(image_path)
    maxsize = (720, 720)

    pillow_image.thumbnail(maxsize)
    buff = BytesIO()
    pillow_image.save(buff, format="JPEG")
    encoded_string = base64.b64encode(buff.getvalue())
    return f"| href=https://www.met.hu/idojaras/aktualis_idojaras/radar/ image={str(encoded_string)[2:][:-1]}"

try:
    current_time = datetime.now()
    hours = 2 if is_summer_time(timezone_name) else 1
    adjusted_time = current_time - timedelta(hours=hours, minutes=10)

    # Round minutes down to the nearest multiple of 5
    rounded_minutes = (adjusted_time.minute // 5) * 5

    # Create a new datetime object with rounded minutes
    rounded_time = adjusted_time.replace(minute=rounded_minutes, second=0, microsecond=0)

    radar_picture = radar_picture(rounded_time)
    radarFeed.append("%s" % (radar_picture))
    #weather_picture = weather_picture(rounded_time)
    #radarFeed.append("%s" % (radar_picture))


except Exception as e:
    print("Couldn't parse response. 💀")
    print(e)
    fallback()
    exit(0)


content = '\n'.join(radarFeed)
print(content)


if not radarFeed:
    print("connection error")
    fallback()

with open(CACHE_FILE, "w+") as f:
    f.write(content)
    f.write("\n---\n")
    f.write("cached\n")
    f.write(time.ctime())
    f.close()
