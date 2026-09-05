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
import urllib.parse
import urllib.request
from typing import Optional

API_URL = "https://api.frankfurter.dev/v2/rate/{base}/{quote}"
REQUIRED_FIELDS = ("rate", "date", "base", "quote")
DEFAULT_BASE1 = "USD"
DEFAULT_BASE2 = "EUR"
DEFAULT_QUOTE = "JPY"


def format_currency_code(currency: str) -> str:
    currency = currency.strip().upper()
    if len(currency) != 3 or not currency.isascii() or not currency.isalpha():
        raise ValueError(f"Invalid currency code: {currency!r}")
    return urllib.parse.quote(currency, safe="")


def validate_rate_data(data: object) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Exchange rate response must be a JSON object")

    missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
    if missing_fields:
        raise ValueError(f"Exchange rate response is missing: {', '.join(missing_fields)}")

    if (
            not isinstance(data["rate"], (int, float))
            or isinstance(data["rate"], bool)
            or not isinstance(data["date"], str)
            or not isinstance(data["base"], str)
            or not isinstance(data["quote"], str)
    ):
        raise ValueError("Exchange rate response contains invalid field types")

    return data


def fetch_rate(base: str, quote: str) -> Optional[dict]:
    try:
        base = format_currency_code(base)
        quote = format_currency_code(quote)
        url = API_URL.format(base=base, quote=quote)
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "xbar/1.0"}
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            return validate_rate_data(json.loads(response.read()))
    except Exception as e:
        print(f"Failed to fetch rate. {e}", file=sys.stderr)
        return None


def main() -> None:
    base1 = os.environ.get("VAR_BASE1", DEFAULT_BASE1)
    base2 = os.environ.get("VAR_BASE2", DEFAULT_BASE2)
    quote = os.environ.get("VAR_QUOTE", DEFAULT_QUOTE)

    for index, base in enumerate((base1, base2)):
        rate_data = fetch_rate(base, quote)
        if not rate_data:
            continue

        if index == 0:
            print(rate_data["rate"])
        print("---")
        print(rate_data["date"])
        print(f"{rate_data['base']} {rate_data['quote']}: {rate_data['rate']}")


if __name__ == "__main__":
    main()
