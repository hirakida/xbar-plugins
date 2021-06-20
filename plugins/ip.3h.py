#!/usr/local/bin/python3

import json
import urllib.error
import urllib.parse
import urllib.request


def main():
    url = "http://ip-api.com/json"
    try:
        with urllib.request.urlopen(url) as response:
            content = json.loads(response.read().decode("utf8"))
            print(content["query"])
            print("---")
            print("as: {0}".format(content["as"]))
            print("isp: {0}".format(content["isp"]))
            print("org: {0}".format(content["org"]))
            print("---")
            print("city: {0}".format(content["city"]))
            print("region: {0}".format(content["regionName"]))
            print("country: {0}".format(content["country"]))
            print("timezone: {0}".format(content["timezone"]))
            print("zip: {0}".format(content["zip"]))
            print("lat: {0}".format(content["lat"]))
            print("lon: {0}".format(content["lon"]))
            print("---")
    except urllib.error.URLError:
        pass


if __name__ == '__main__':
    main()
