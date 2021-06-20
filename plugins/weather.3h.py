#!/usr/local/bin/python3
# coding=utf-8

import datetime
import json
import urllib.error
import urllib.parse
import urllib.request

AREA_CODE = 400000
CHILD_AREA_CODE = 400010
TEMPS_CODE = 82182


def main():
    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    now = datetime.datetime.now(jst)

    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json".format(AREA_CODE)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            content = json.loads(response.read().decode("utf8"))
            time_series = content[0]["timeSeries"]
            time_defines0 = time_series[0]["timeDefines"]
            time_defines2 = time_series[2]["timeDefines"]
            areas0 = time_series[0]["areas"]
            areas2 = time_series[2]["areas"]

            times0 = [datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z") for time in time_defines0]
            temps = {}
            for area2 in areas2:
                if area2["area"]["code"] == str(TEMPS_CODE):
                    for time, temp in zip(time_defines2, area2["temps"]):
                        temp_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
                        temps[temp_time] = temp

            for area0 in areas0:
                if area0["area"]["code"] == str(CHILD_AREA_CODE):
                    for index0, (time0, weather) in enumerate(zip(times0, area0["weathers"])):
                        if index0 == 0:
                            print("{}".format(weather))
                            print("---")
                        print("{}".format(time0.date()))
                        print("{}".format(weather))

                        for key, value in temps.items():
                            if key.date() == time0.date():
                                if key.time() == datetime.time(0, 0):
                                    if key > now:
                                        print("Min: {} | color=blue".format(value))
                                else:
                                    print("Max: {} | color=red".format(value))
                        print("---")
    except urllib.error.URLError:
        pass

    web_url = "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code={}".format(AREA_CODE)
    print("Website... | href={}".format(web_url))


if __name__ == '__main__':
    main()
