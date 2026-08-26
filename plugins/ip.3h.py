#!/usr/bin/env python3

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
            data = response.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.URLError as e:
        print(f"Failed to fetch {API_URL}. {e}", file=sys.stderr)
        return None


def main():
    content = fetch_data()
    if content:
        print(content["query"])
        print("---")
        print(f"as: {content['as']}")
        print(f"isp: {content['isp']}")
        print(f"org: {content['org']}")
        print("---")
        print(f"city: {content['city']}")
        print(f"region: {content['regionName']}")
        print(f"country: {content['country']}")
        print(f"timezone: {content['timezone']}")
        print(f"zip: {content['zip']}")
        print(f"lat: {content['lat']}")
        print(f"lon: {content['lon']}")
        print("---")


if __name__ == "__main__":
    main()
