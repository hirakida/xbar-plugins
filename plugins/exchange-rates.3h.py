#!/usr/bin/env python3

#  <xbar.title>Exchange rates</xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>hirakida</xbar.author>
#  <xbar.author.github>hirakida</xbar.author.github>
#  <xbar.desc>Displays exchange rates.</xbar.desc>
#  <xbar.image>https://avatars.githubusercontent.com/u/12070156</xbar.image>
#  <xbar.dependencies>python</xbar.dependencies>
#  <xbar.abouturl>https://github.com/hirakida/xbar-plugins</xbar.abouturl>
#  <xbar.var>string(VAR_BASE1="USD"): The first base currency.</xbar.var>
#  <xbar.var>string(VAR_BASE2="EUR"): The second base currency.</xbar.var>
#  <xbar.var>string(VAR_QUOTE="JPY"): The quote currency.</xbar.var>

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

API_URL = "https://api.frankfurter.dev/v2/rate/{base}/{quote}"


def fetch_data(base: str, quote: str) -> Optional[dict]:
    url = API_URL.format(base=base, quote=quote)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "xbar/1.0"}
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())
    except urllib.error.URLError as e:
        print(f"Failed to fetch {url}. {e}", file=sys.stderr)
        return None


def main():
    base1 = os.environ["VAR_BASE1"]
    base2 = os.environ["VAR_BASE2"]
    quote = os.environ["VAR_QUOTE"]

    content = fetch_data(base1, quote)
    if content:
        print(content["rate"])
        print("---")
        print(content["date"])
        print(f"{content['base']} {content['quote']}: {content['rate']}")
        print("---")

    content = fetch_data(base2, quote)
    if content:
        print(content["date"])
        print(f"{content['base']} {content['quote']}: {content['rate']}")


if __name__ == "__main__":
    main()
