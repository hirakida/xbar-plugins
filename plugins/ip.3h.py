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
import urllib.request
from typing import Optional

API_URL = "http://ip-api.com/json"


def validate_data(data: object) -> dict:
    if not isinstance(data, dict):
        raise ValueError("IP response must be a JSON object")

    if data.get("status") != "success":
        raise ValueError(data.get("message", "IP lookup failed"))

    if not isinstance(data.get("query"), str) or not data["query"]:
        raise ValueError("IP response is missing query")

    return data


def fetch_data() -> Optional[dict]:
    try:
        with urllib.request.urlopen(API_URL, timeout=5) as response:
            return validate_data(json.loads(response.read()))
    except Exception as e:
        print(f"Failed to fetch {API_URL}. {e}", file=sys.stderr)
        return None


def main() -> None:
    data = fetch_data()
    if data:
        print(data["query"])
        print("---")

        fields = (
            "country",
            "regionName",
            "city",
            "zip",
            "lat",
            "lon",
            "timezone",
            "isp",
            "org",
            "as",
        )
        for key in fields:
            value = data.get(key)
            if value is not None and value != "":
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()
