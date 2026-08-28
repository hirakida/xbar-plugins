#!/usr/bin/env python3

#  <xbar.title>Weather forecast</xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>hirakida</xbar.author>
#  <xbar.author.github>hirakida</xbar.author.github>
#  <xbar.desc>Displays the weather forecast.</xbar.desc>
#  <xbar.image>https://avatars.githubusercontent.com/u/12070156</xbar.image>
#  <xbar.dependencies>python</xbar.dependencies>
#  <xbar.abouturl>https://github.com/hirakida/xbar-plugins</xbar.abouturl>
#  <xbar.var>string(VAR_AREA_CODE="400000"): The area code.</xbar.var>
#  <xbar.var>string(VAR_REGION_AREA_CODE="400010"): The region area code.</xbar.var>
#  <xbar.var>string(VAR_CITY_AREA_CODE="82182"): The city area code.</xbar.var>

import base64
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional
from zoneinfo import ZoneInfo

TELOPS = """
{
    "100": [
        "100.svg",
        "500.svg",
        "100",
        "晴",
        "CLEAR"
    ],
    "101": [
        "101.svg",
        "501.svg",
        "100",
        "晴時々曇",
        "PARTLY CLOUDY"
    ],
    "102": [
        "102.svg",
        "502.svg",
        "300",
        "晴一時雨",
        "CLEAR, OCCASIONAL SCATTERED SHOWERS"
    ],
    "103": [
        "102.svg",
        "502.svg",
        "300",
        "晴時々雨",
        "CLEAR, FREQUENT SCATTERED SHOWERS"
    ],
    "104": [
        "104.svg",
        "504.svg",
        "400",
        "晴一時雪",
        "CLEAR, SNOW FLURRIES"
    ],
    "105": [
        "104.svg",
        "504.svg",
        "400",
        "晴時々雪",
        "CLEAR, FREQUENT SNOW FLURRIES"
    ],
    "106": [
        "102.svg",
        "502.svg",
        "300",
        "晴一時雨か雪",
        "CLEAR, OCCASIONAL SCATTERED SHOWERS OR SNOW FLURRIES"
    ],
    "107": [
        "102.svg",
        "502.svg",
        "300",
        "晴時々雨か雪",
        "CLEAR, FREQUENT SCATTERED SHOWERS OR SNOW FLURRIES"
    ],
    "108": [
        "102.svg",
        "502.svg",
        "300",
        "晴一時雨か雷雨",
        "CLEAR, OCCASIONAL SCATTERED SHOWERS AND/OR THUNDER"
    ],
    "110": [
        "110.svg",
        "510.svg",
        "100",
        "晴後時々曇",
        "CLEAR, PARTLY CLOUDY LATER"
    ],
    "111": [
        "110.svg",
        "510.svg",
        "100",
        "晴後曇",
        "CLEAR, CLOUDY LATER"
    ],
    "112": [
        "112.svg",
        "512.svg",
        "300",
        "晴後一時雨",
        "CLEAR, OCCASIONAL SCATTERED SHOWERS LATER"
    ],
    "113": [
        "112.svg",
        "512.svg",
        "300",
        "晴後時々雨",
        "CLEAR, FREQUENT SCATTERED SHOWERS LATER"
    ],
    "114": [
        "112.svg",
        "512.svg",
        "300",
        "晴後雨",
        "CLEAR,RAIN LATER"
    ],
    "115": [
        "115.svg",
        "515.svg",
        "400",
        "晴後一時雪",
        "CLEAR, OCCASIONAL SNOW FLURRIES LATER"
    ],
    "116": [
        "115.svg",
        "515.svg",
        "400",
        "晴後時々雪",
        "CLEAR, FREQUENT SNOW FLURRIES LATER"
    ],
    "117": [
        "115.svg",
        "515.svg",
        "400",
        "晴後雪",
        "CLEAR,SNOW LATER"
    ],
    "118": [
        "112.svg",
        "512.svg",
        "300",
        "晴後雨か雪",
        "CLEAR, RAIN OR SNOW LATER"
    ],
    "119": [
        "112.svg",
        "512.svg",
        "300",
        "晴後雨か雷雨",
        "CLEAR, RAIN AND/OR THUNDER LATER"
    ],
    "120": [
        "102.svg",
        "502.svg",
        "300",
        "晴朝夕一時雨",
        "OCCASIONAL SCATTERED SHOWERS IN THE MORNING AND EVENING, CLEAR DURING THE DAY"
    ],
    "121": [
        "102.svg",
        "502.svg",
        "300",
        "晴朝の内一時雨",
        "OCCASIONAL SCATTERED SHOWERS IN THE MORNING, CLEAR DURING THE DAY"
    ],
    "122": [
        "112.svg",
        "512.svg",
        "300",
        "晴夕方一時雨",
        "CLEAR, OCCASIONAL SCATTERED SHOWERS IN THE EVENING"
    ],
    "123": [
        "100.svg",
        "500.svg",
        "100",
        "晴山沿い雷雨",
        "CLEAR IN THE PLAINS, RAIN AND THUNDER NEAR MOUTAINOUS AREAS"
    ],
    "124": [
        "100.svg",
        "500.svg",
        "100",
        "晴山沿い雪",
        "CLEAR IN THE PLAINS, SNOW NEAR MOUTAINOUS AREAS"
    ],
    "125": [
        "112.svg",
        "512.svg",
        "300",
        "晴午後は雷雨",
        "CLEAR, RAIN AND THUNDER IN THE AFTERNOON"
    ],
    "126": [
        "112.svg",
        "512.svg",
        "300",
        "晴昼頃から雨",
        "CLEAR, RAIN IN THE AFTERNOON"
    ],
    "127": [
        "112.svg",
        "512.svg",
        "300",
        "晴夕方から雨",
        "CLEAR, RAIN IN THE EVENING"
    ],
    "128": [
        "112.svg",
        "512.svg",
        "300",
        "晴夜は雨",
        "CLEAR, RAIN IN THE NIGHT"
    ],
    "130": [
        "100.svg",
        "500.svg",
        "100",
        "朝の内霧後晴",
        "FOG IN THE MORNING, CLEAR LATER"
    ],
    "131": [
        "100.svg",
        "500.svg",
        "100",
        "晴明け方霧",
        "FOG AROUND DAWN, CLEAR LATER"
    ],
    "132": [
        "101.svg",
        "501.svg",
        "100",
        "晴朝夕曇",
        "CLOUDY IN THE MORNING AND EVENING, CLEAR DURING THE DAY"
    ],
    "140": [
        "102.svg",
        "502.svg",
        "300",
        "晴時々雨で雷を伴う",
        "CLEAR, FREQUENT SCATTERED SHOWERS AND THUNDER"
    ],
    "160": [
        "104.svg",
        "504.svg",
        "400",
        "晴一時雪か雨",
        "CLEAR, SNOW FLURRIES OR OCCASIONAL SCATTERED SHOWERS"
    ],
    "170": [
        "104.svg",
        "504.svg",
        "400",
        "晴時々雪か雨",
        "CLEAR, FREQUENT SNOW FLURRIES OR SCATTERED SHOWERS"
    ],
    "181": [
        "115.svg",
        "515.svg",
        "400",
        "晴後雪か雨",
        "CLEAR, SNOW OR RAIN LATER"
    ],
    "200": [
        "200.svg",
        "200.svg",
        "200",
        "曇",
        "CLOUDY"
    ],
    "201": [
        "201.svg",
        "601.svg",
        "200",
        "曇時々晴",
        "MOSTLY CLOUDY"
    ],
    "202": [
        "202.svg",
        "202.svg",
        "300",
        "曇一時雨",
        "CLOUDY, OCCASIONAL SCATTERED SHOWERS"
    ],
    "203": [
        "202.svg",
        "202.svg",
        "300",
        "曇時々雨",
        "CLOUDY, FREQUENT SCATTERED SHOWERS"
    ],
    "204": [
        "204.svg",
        "204.svg",
        "400",
        "曇一時雪",
        "CLOUDY, OCCASIONAL SNOW FLURRIES"
    ],
    "205": [
        "204.svg",
        "204.svg",
        "400",
        "曇時々雪",
        "CLOUDY FREQUENT SNOW FLURRIES"
    ],
    "206": [
        "202.svg",
        "202.svg",
        "300",
        "曇一時雨か雪",
        "CLOUDY, OCCASIONAL SCATTERED SHOWERS OR SNOW FLURRIES"
    ],
    "207": [
        "202.svg",
        "202.svg",
        "300",
        "曇時々雨か雪",
        "CLOUDY, FREQUENT SCCATERED SHOWERS OR SNOW FLURRIES"
    ],
    "208": [
        "202.svg",
        "202.svg",
        "300",
        "曇一時雨か雷雨",
        "CLOUDY, OCCASIONAL SCATTERED SHOWERS AND/OR THUNDER"
    ],
    "209": [
        "200.svg",
        "200.svg",
        "200",
        "霧",
        "FOG"
    ],
    "210": [
        "210.svg",
        "610.svg",
        "200",
        "曇後時々晴",
        "CLOUDY, PARTLY CLOUDY LATER"
    ],
    "211": [
        "210.svg",
        "610.svg",
        "200",
        "曇後晴",
        "CLOUDY, CLEAR LATER"
    ],
    "212": [
        "212.svg",
        "212.svg",
        "300",
        "曇後一時雨",
        "CLOUDY, OCCASIONAL SCATTERED SHOWERS LATER"
    ],
    "213": [
        "212.svg",
        "212.svg",
        "300",
        "曇後時々雨",
        "CLOUDY, FREQUENT SCATTERED SHOWERS LATER"
    ],
    "214": [
        "212.svg",
        "212.svg",
        "300",
        "曇後雨",
        "CLOUDY, RAIN LATER"
    ],
    "215": [
        "215.svg",
        "215.svg",
        "400",
        "曇後一時雪",
        "CLOUDY, SNOW FLURRIES LATER"
    ],
    "216": [
        "215.svg",
        "215.svg",
        "400",
        "曇後時々雪",
        "CLOUDY, FREQUENT SNOW FLURRIES LATER"
    ],
    "217": [
        "215.svg",
        "215.svg",
        "400",
        "曇後雪",
        "CLOUDY, SNOW LATER"
    ],
    "218": [
        "212.svg",
        "212.svg",
        "300",
        "曇後雨か雪",
        "CLOUDY, RAIN OR SNOW LATER"
    ],
    "219": [
        "212.svg",
        "212.svg",
        "300",
        "曇後雨か雷雨",
        "CLOUDY, RAIN AND/OR THUNDER LATER"
    ],
    "220": [
        "202.svg",
        "202.svg",
        "300",
        "曇朝夕一時雨",
        "OCCASIONAL SCCATERED SHOWERS IN THE MORNING AND EVENING, CLOUDY DURING THE DAY"
    ],
    "221": [
        "202.svg",
        "202.svg",
        "300",
        "曇朝の内一時雨",
        "CLOUDY OCCASIONAL SCCATERED SHOWERS IN THE MORNING"
    ],
    "222": [
        "212.svg",
        "212.svg",
        "300",
        "曇夕方一時雨",
        "CLOUDY, OCCASIONAL SCCATERED SHOWERS IN THE EVENING"
    ],
    "223": [
        "201.svg",
        "601.svg",
        "200",
        "曇日中時々晴",
        "CLOUDY IN THE MORNING AND EVENING, PARTLY CLOUDY DURING THE DAY,"
    ],
    "224": [
        "212.svg",
        "212.svg",
        "300",
        "曇昼頃から雨",
        "CLOUDY, RAIN IN THE AFTERNOON"
    ],
    "225": [
        "212.svg",
        "212.svg",
        "300",
        "曇夕方から雨",
        "CLOUDY, RAIN IN THE EVENING"
    ],
    "226": [
        "212.svg",
        "212.svg",
        "300",
        "曇夜は雨",
        "CLOUDY, RAIN IN THE NIGHT"
    ],
    "228": [
        "215.svg",
        "215.svg",
        "400",
        "曇昼頃から雪",
        "CLOUDY, SNOW IN THE AFTERNOON"
    ],
    "229": [
        "215.svg",
        "215.svg",
        "400",
        "曇夕方から雪",
        "CLOUDY, SNOW IN THE EVENING"
    ],
    "230": [
        "215.svg",
        "215.svg",
        "400",
        "曇夜は雪",
        "CLOUDY, SNOW IN THE NIGHT"
    ],
    "231": [
        "200.svg",
        "200.svg",
        "200",
        "曇海上海岸は霧か霧雨",
        "CLOUDY, FOG OR DRIZZLING ON THE SEA AND NEAR SEASHORE"
    ],
    "240": [
        "202.svg",
        "202.svg",
        "300",
        "曇時々雨で雷を伴う",
        "CLOUDY, FREQUENT SCCATERED SHOWERS AND THUNDER"
    ],
    "250": [
        "204.svg",
        "204.svg",
        "400",
        "曇時々雪で雷を伴う",
        "CLOUDY, FREQUENT SNOW AND THUNDER"
    ],
    "260": [
        "204.svg",
        "204.svg",
        "400",
        "曇一時雪か雨",
        "CLOUDY, SNOW FLURRIES OR OCCASIONAL SCATTERED SHOWERS"
    ],
    "270": [
        "204.svg",
        "204.svg",
        "400",
        "曇時々雪か雨",
        "CLOUDY, FREQUENT SNOW FLURRIES OR SCATTERED SHOWERS"
    ],
    "281": [
        "215.svg",
        "215.svg",
        "400",
        "曇後雪か雨",
        "CLOUDY, SNOW OR RAIN LATER"
    ],
    "300": [
        "300.svg",
        "300.svg",
        "300",
        "雨",
        "RAIN"
    ],
    "301": [
        "301.svg",
        "701.svg",
        "300",
        "雨時々晴",
        "RAIN, PARTLY CLOUDY"
    ],
    "302": [
        "302.svg",
        "302.svg",
        "300",
        "雨時々止む",
        "SHOWERS THROUGHOUT THE DAY"
    ],
    "303": [
        "303.svg",
        "303.svg",
        "400",
        "雨時々雪",
        "RAIN,FREQUENT SNOW FLURRIES"
    ],
    "304": [
        "300.svg",
        "300.svg",
        "300",
        "雨か雪",
        "RAINORSNOW"
    ],
    "306": [
        "300.svg",
        "300.svg",
        "300",
        "大雨",
        "HEAVYRAIN"
    ],
    "308": [
        "308.svg",
        "308.svg",
        "300",
        "雨で暴風を伴う",
        "RAINSTORM"
    ],
    "309": [
        "303.svg",
        "303.svg",
        "400",
        "雨一時雪",
        "RAIN,OCCASIONAL SNOW"
    ],
    "311": [
        "311.svg",
        "711.svg",
        "300",
        "雨後晴",
        "RAIN,CLEAR LATER"
    ],
    "313": [
        "313.svg",
        "313.svg",
        "300",
        "雨後曇",
        "RAIN,CLOUDY LATER"
    ],
    "314": [
        "314.svg",
        "314.svg",
        "400",
        "雨後時々雪",
        "RAIN, FREQUENT SNOW FLURRIES LATER"
    ],
    "315": [
        "314.svg",
        "314.svg",
        "400",
        "雨後雪",
        "RAIN,SNOW LATER"
    ],
    "316": [
        "311.svg",
        "711.svg",
        "300",
        "雨か雪後晴",
        "RAIN OR SNOW, CLEAR LATER"
    ],
    "317": [
        "313.svg",
        "313.svg",
        "300",
        "雨か雪後曇",
        "RAIN OR SNOW, CLOUDY LATER"
    ],
    "320": [
        "311.svg",
        "711.svg",
        "300",
        "朝の内雨後晴",
        "RAIN IN THE MORNING, CLEAR LATER"
    ],
    "321": [
        "313.svg",
        "313.svg",
        "300",
        "朝の内雨後曇",
        "RAIN IN THE MORNING, CLOUDY LATER"
    ],
    "322": [
        "303.svg",
        "303.svg",
        "400",
        "雨朝晩一時雪",
        "OCCASIONAL SNOW IN THE MORNING AND EVENING, RAIN DURING THE DAY"
    ],
    "323": [
        "311.svg",
        "711.svg",
        "300",
        "雨昼頃から晴",
        "RAIN, CLEAR IN THE AFTERNOON"
    ],
    "324": [
        "311.svg",
        "711.svg",
        "300",
        "雨夕方から晴",
        "RAIN, CLEAR IN THE EVENING"
    ],
    "325": [
        "311.svg",
        "711.svg",
        "300",
        "雨夜は晴",
        "RAIN, CLEAR IN THE NIGHT"
    ],
    "326": [
        "314.svg",
        "314.svg",
        "400",
        "雨夕方から雪",
        "RAIN, SNOW IN THE EVENING"
    ],
    "327": [
        "314.svg",
        "314.svg",
        "400",
        "雨夜は雪",
        "RAIN,SNOW IN THE NIGHT"
    ],
    "328": [
        "300.svg",
        "300.svg",
        "300",
        "雨一時強く降る",
        "RAIN, EXPECT OCCASIONAL HEAVY RAINFALL"
    ],
    "329": [
        "300.svg",
        "300.svg",
        "300",
        "雨一時みぞれ",
        "RAIN, OCCASIONAL SLEET"
    ],
    "340": [
        "400.svg",
        "400.svg",
        "400",
        "雪か雨",
        "SNOWORRAIN"
    ],
    "350": [
        "300.svg",
        "300.svg",
        "300",
        "雨で雷を伴う",
        "RAIN AND THUNDER"
    ],
    "361": [
        "411.svg",
        "811.svg",
        "400",
        "雪か雨後晴",
        "SNOW OR RAIN, CLEAR LATER"
    ],
    "371": [
        "413.svg",
        "413.svg",
        "400",
        "雪か雨後曇",
        "SNOW OR RAIN, CLOUDY LATER"
    ],
    "400": [
        "400.svg",
        "400.svg",
        "400",
        "雪",
        "SNOW"
    ],
    "401": [
        "401.svg",
        "801.svg",
        "400",
        "雪時々晴",
        "SNOW, FREQUENT CLEAR"
    ],
    "402": [
        "402.svg",
        "402.svg",
        "400",
        "雪時々止む",
        "SNOWTHROUGHOUT THE DAY"
    ],
    "403": [
        "403.svg",
        "403.svg",
        "400",
        "雪時々雨",
        "SNOW,FREQUENT SCCATERED SHOWERS"
    ],
    "405": [
        "400.svg",
        "400.svg",
        "400",
        "大雪",
        "HEAVYSNOW"
    ],
    "406": [
        "406.svg",
        "406.svg",
        "400",
        "風雪強い",
        "SNOWSTORM"
    ],
    "407": [
        "406.svg",
        "406.svg",
        "400",
        "暴風雪",
        "HEAVYSNOWSTORM"
    ],
    "409": [
        "403.svg",
        "403.svg",
        "400",
        "雪一時雨",
        "SNOW, OCCASIONAL SCCATERED SHOWERS"
    ],
    "411": [
        "411.svg",
        "811.svg",
        "400",
        "雪後晴",
        "SNOW,CLEAR LATER"
    ],
    "413": [
        "413.svg",
        "413.svg",
        "400",
        "雪後曇",
        "SNOW,CLOUDY LATER"
    ],
    "414": [
        "414.svg",
        "414.svg",
        "400",
        "雪後雨",
        "SNOW,RAIN LATER"
    ],
    "420": [
        "411.svg",
        "811.svg",
        "400",
        "朝の内雪後晴",
        "SNOW IN THE MORNING, CLEAR LATER"
    ],
    "421": [
        "413.svg",
        "413.svg",
        "400",
        "朝の内雪後曇",
        "SNOW IN THE MORNING, CLOUDY LATER"
    ],
    "422": [
        "414.svg",
        "414.svg",
        "400",
        "雪昼頃から雨",
        "SNOW, RAIN IN THE AFTERNOON"
    ],
    "423": [
        "414.svg",
        "414.svg",
        "400",
        "雪夕方から雨",
        "SNOW, RAIN IN THE EVENING"
    ],
    "425": [
        "400.svg",
        "400.svg",
        "400",
        "雪一時強く降る",
        "SNOW, EXPECT OCCASIONAL HEAVY SNOWFALL"
    ],
    "426": [
        "400.svg",
        "400.svg",
        "400",
        "雪後みぞれ",
        "SNOW, SLEET LATER"
    ],
    "427": [
        "400.svg",
        "400.svg",
        "400",
        "雪一時みぞれ",
        "SNOW, OCCASIONAL SLEET"
    ],
    "450": [
        "400.svg",
        "400.svg",
        "400",
        "雪で雷を伴う",
        "SNOW AND THUNDER"
    ]
}
"""

API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
WEB_URL = "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code={area_code}"
ICON_URL = "https://www.jma.go.jp/bosai/forecast/img/{icon_name}"
CACHE_FILE = "/tmp/xbar_{icon_name}"


def fetch_data(area_code: str) -> Optional[dict]:
    url = API_URL.format(area_code=area_code)
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except urllib.error.URLError as e:
        print(f"Failed to fetch {url}. {e}", file=sys.stderr)
        return None


def convert_to_datetime(time: str) -> datetime.datetime:
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")


def get_weather_text(weather_code: str) -> str:
    telops = json.loads(TELOPS)
    return telops[weather_code][3]


def get_base64_icon(weather_code: str) -> Optional[str]:
    telops = json.loads(TELOPS)
    icon_name = telops[weather_code][0]
    icon_url = ICON_URL.format(icon_name=icon_name)
    cache_path = CACHE_FILE.format(icon_name=icon_name)

    if not os.path.exists(cache_path):
        try:
            urllib.request.urlretrieve(icon_url, cache_path)
        except urllib.error.URLError as e:
            print(f"Failed to retrieve {icon_url}. {e}", file=sys.stderr)
            return None

    try:
        with open(cache_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except OSError as e:
        print(f"Failed to open {cache_path}. {e}", file=sys.stderr)
        return None


def main():
    area_code = os.environ["VAR_AREA_CODE"]
    region_area_code = os.environ["VAR_REGION_AREA_CODE"]
    city_area_code = os.environ["VAR_CITY_AREA_CODE"]

    content = fetch_data(area_code)
    if content:
        now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
        time_series = content[0]["timeSeries"]
        weather_series = time_series[0]
        pop_series = time_series[1]
        temp_series = time_series[2]

        # key=datetime, value=pop
        pops = {}
        for pop_area in pop_series["areas"]:
            if pop_area["area"]["code"] == region_area_code:
                for time_define, pop in zip(pop_series["timeDefines"], pop_area["pops"]):
                    pop_datetime = convert_to_datetime(time_define)
                    pops[pop_datetime] = pop

        # key=datetime, value=temp
        temps = {}
        for temp_area in temp_series["areas"]:
            if temp_area["area"]["code"] == city_area_code:
                for time_define, temp in zip(temp_series["timeDefines"], temp_area["temps"]):
                    temp_datetime = convert_to_datetime(time_define)
                    temps[temp_datetime] = temp

        for weather_area in weather_series["areas"]:
            if weather_area["area"]["code"] == region_area_code:
                for index, (time_define, weather_code, weather) in enumerate(
                        zip(weather_series["timeDefines"], weather_area["weatherCodes"], weather_area["weathers"])):
                    if index == 0:
                        print(get_weather_text(weather_code))
                        print("---")
                    weather_datetime = convert_to_datetime(time_define)
                    print(weather_datetime.date())
                    print(weather)

                    pop_list = []
                    for pop_datetime, pop in pops.items():
                        if pop_datetime.date() == weather_datetime.date():
                            pop_list.append(f"{pop_datetime.hour:02d}h({pop}%)")
                    pop_text = " ,".join(pop_list)
                    print(f"PoP: {pop_text}")

                    for temp_datetime, temp in temps.items():
                        if temp_datetime.date() == weather_datetime.date():
                            if temp_datetime.time() == datetime.time(0, 0):
                                if temp_datetime > now:
                                    print(f"Min: {temp} | color=blue")
                            else:
                                print(f"Max: {temp} | color=red")
                    print("---")

    web_url = WEB_URL.format(area_code=area_code)
    print(f"Website... | href={web_url}")


if __name__ == "__main__":
    main()
