#!/usr/bin/env python3

#  <xbar.title>IP address</xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>hirakida</xbar.author>
#  <xbar.author.github>hirakida</xbar.author.github>
#  <xbar.desc>Displays IP address.</xbar.desc>
#  <xbar.image>https://avatars.githubusercontent.com/u/12070156</xbar.image>
#  <xbar.dependencies>python</xbar.dependencies>
#  <xbar.abouturl>https://github.com/hirakida/xbar-plugins</xbar.abouturl>

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

API_URL = "http://ip-api.com/json"


def fetch_data() -> Optional[dict]:
    try:
        with urllib.request.urlopen(API_URL) as response:
            return json.loads(response.read())
    except urllib.error.URLError as e:
        print(f"Failed to fetch {API_URL}. {e}", file=sys.stderr)
        return None


def main():
    content = fetch_data()
    if content:
        print(content["query"])
        print("---")
        print(f"country: {content['country']}")
        print(f"region: {content['regionName']}")
        print(f"city: {content['city']}")
        print(f"zip: {content['zip']}")
        print(f"lat: {content['lat']}")
        print(f"lon: {content['lon']}")
        print(f"timezone: {content['timezone']}")
        print(f"isp: {content['isp']}")
        print(f"org: {content['org']}")
        print(f"as: {content['as']}")
        print("---")


if __name__ == "__main__":
    main()
