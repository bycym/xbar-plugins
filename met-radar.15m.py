#!/usr/bin/python3
# -*- coding: utf-8 -*-


# May need to pip(3) install pillow
# /usr/bin/python3 -m pip install cairosvg pillow beautifulsoup4
# May need to install certificates: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
import base64
import urllib.request
from PIL import Image
import io
from io import BytesIO

import datetime
import time
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

print('🔭')
print('---')
print('Refresh... | refresh=true')
img_prefix = "RccW"
CACHE_FILE="not/radar.cache"
radarFeed = []
headers = {'accept': 'application/xml;q=0.9, */*;q=0.8'}
timezone_name = "Europe/Budapest"
max_day_weather = 5

# ☀️☁️⛅⛈️🌤️🌥️🌦️🌧️🌨️🌩️⚡❄️
emoji_dict = {
    10: "☀️", # derült
    21: "⛅", # gyengén felhős
    321: "⛅", # gyengén felhős
    22: "🌥️", # közepesen felhős
    23: "☁️", # erősen felhős
    26: "☁️", # erősen felhős
    27: "5", # 
    29: "6", # 
    30: "☁️", # borult
    42: "🌦️", # gyenge eső
    81: "🌧️", # zápor
    90: "⛈️", # zivatar
}

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
    
    # 2: means remove the "b'" from the beggining and :-1 remove the end "'"
    return f"| href=https://www.met.hu/idojaras/aktualis_idojaras/radar/ image={str(encoded_string)[2:][:-1]}" 


def daily_weather() -> list:
    import urllib.request
    from bs4 import BeautifulSoup

    location = "veszprem"
    url = f"https://www.idokep.hu/elorejelzes/{location}"
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="ik daily-forecast-container dailyForecastBiggerContainer")
    if not container:
        return ["| text=No forecast found"]

    results = []
    daily_forecast_count = 0
    for col in container.find_all("div", class_="ik dailyForecastCol"):
        if(daily_forecast_count >= max_day_weather):
            break
        daily_forecast_count += 1
        weather_description = extract_description_from_col(col, "ik d-block w-100 ik interact")

        # Find min and max
        min_div = col.find("div", class_="ik min")
        max_div = col.find("div", class_="ik max")
        day = col.find("span", class_="ik dfDay").text.strip() if col.find("span", class_="ik dfDay") else col.find("span", class_="ik dfDay vacation").text.strip()
        day_num = col.find("span", class_="ik dfDayNum").text.strip() if col.find("span", class_="ik dfDayNum") else col.find("span", class_="ik dfDayNum vacation").text.strip()
        min_val = min_div.find("a").text.strip() if min_div and min_div.find("a") else "?"
        max_val = max_div.find("a").text.strip() if max_div and max_div.find("a") else "?"

        # Find all icons (svg/png)
        icons = []
        weather_emoji = ""
        for img in col.find_all("img"):
            src = img.get('src', '')
            if src.endswith('.svg'):
                icon_path = int(src.split('/')[-1].split('.')[0])
                weather_emoji = emoji_dict.get(icon_path, "")


        # results.append(f"min: {min_val} - max: {max_val}, {', '.join(icons)} | base64: {', '.join([b for b in icons_b64 if b])}")
        results.append(f"{weather_emoji} [{day_num}:{day}] ~ 🔻: {min_val} - 🔺: {max_val} [{weather_description}]|href=asd")
    return results

def hourly_weather() -> list:
    import urllib.request
    from bs4 import BeautifulSoup

    location = "veszprem"
    url = f"https://www.idokep.hu/elorejelzes/{location}"
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="ik new-hourly-forecast-card-container")
    if not container:
        return ["| text=No forecast found"]

    results = []
    hourly_forecast_count = 0
    for col in container.find_all("div", class_="ik new-hourly-forecast-card"):
        if(hourly_forecast_count >= max_day_weather):
            break
        hourly_forecast_count += 1
        weather_description = extract_description_from_col(col, "ik d-block w-100 hover-over")

        temperature = col.find("a", class_="ik hover-over d-block").text.strip()
        hour = col.find("div", class_="new-hourly-forecast-hour").text.strip()

        weather_emoji = ""
        for img in col.find_all("img"):
            src = img.get('src', '')
            if src.endswith('.svg'):
                if( not src.startswith('/assets/forecast-icons/')):
                    continue
                icon_path = int(src.split('/')[-1].split('.')[0])
                # print(f"icon_path: {icon_path} :: {weather_description}")
                weather_emoji = emoji_dict.get(icon_path, "")

        # results.append(f"min: {min_val} - max: {max_val}, {', '.join(icons)} | base64: {', '.join([b for b in icons_b64 if b])}")
        results.append(f"{weather_emoji} [{hour}] ~ {temperature} [{weather_description}]|href=asd")
    return results

def extract_description_from_col(col, class_name):
    # Find the <a> tag with the relevant class
    a_tag = col.find("a", class_ = class_name)
    if not a_tag:
        return None

    # Get the data-bs-content attribute (contains HTML as a string)
    data_bs_content = a_tag.get("data-bs-content", "")
    if not data_bs_content:
        return None

    # Parse the HTML inside data-bs-content
    inner_soup = BeautifulSoup(data_bs_content, "html.parser")
    # If there are no tags, it's just plain text
    if not inner_soup.find():
        return data_bs_content.strip()
    # Find all divs with class 'ik fc-line'
    fc_lines = inner_soup.find_all("div", class_="ik fc-line")
    for fc in fc_lines:
        text = fc.get_text(strip=True)
        return text 
    return None

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
    
    radarFeed.append("%s" % ("---"))
    hourly_weather = "\n".join(hourly_weather())
    radarFeed.append("%s" % (hourly_weather))
    radarFeed.append("%s" % ("---"))
    daily_weather = "\n".join(daily_weather())
    radarFeed.append("%s" % (daily_weather))
    radarFeed.append("%s" % ("---"))


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

with open(CACHE_FILE, "w+", encoding="utf-8") as f:
    f.write(content)
    f.write("\n---\n")
    f.write("cached\n")
    f.write(time.ctime())
    f.close()
