#!/usr/bin/env python3

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

API_URL = "https://api.frankfurter.dev/v2/rate/{base}/JPY"
USD = "USD"
EUR = "EUR"


def main():
    content = fetch_data(USD)
    if content:
        print(content["rate"])
        print("---")
        print(content["date"])
        print(f"{content['base']} {content['quote']}: {content['rate']}")
        print("---")

    content = fetch_data(EUR)
    if content:
        print(content["date"])
        print(f"{content['base']} {content['quote']}: {content['rate']}")


def fetch_data(base: str) -> Optional[dict]:
    request = urllib.request.Request(
        API_URL.format(base=base),
        headers={"User-Agent": "xbar/1.0"}
    )
    try:
        with urllib.request.urlopen(request) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.URLError as e:
        print(f"Failed to fetch {API_URL}. {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    main()
