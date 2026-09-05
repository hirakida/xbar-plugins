#!/usr/bin/env python3

#  <xbar.title>GitHub Notifications</xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>hirakida</xbar.author>
#  <xbar.author.github>hirakida</xbar.author.github>
#  <xbar.desc>Displays GitHub notifications.</xbar.desc>
#  <xbar.image>https://avatars.githubusercontent.com/u/12070156</xbar.image>
#  <xbar.dependencies>python</xbar.dependencies>
#  <xbar.abouturl>https://github.com/hirakida/xbar-plugins</xbar.abouturl>
#  <xbar.var>string(VAR_GITHUB_TOKEN=""): GitHub personal access token(classic).</xbar.var>
#  <xbar.var>boolean(VAR_NOTIFICATIONS_ALL=false): If true, show notifications marked as read.</xbar.var>

import json
import os
import sys
import urllib.request
from typing import Optional

API_URL = "https://api.github.com/notifications?all={all}"
WEB_URL = "https://github.com/notifications"


def fetch_data() -> Optional[dict]:
    token = os.environ["VAR_GITHUB_TOKEN"]
    include_all = os.environ["VAR_NOTIFICATIONS_ALL"]
    url = API_URL.format(all=include_all)

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "xbar/1.0",
        }
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Failed to fetch {url}. {e}", file=sys.stderr)
        return None


def get_web_url(notification: dict) -> str:
    subject = notification["subject"]
    subject_type = subject["type"]
    url = subject["url"]

    if subject_type == "PullRequest":
        return url.replace(
            "https://api.github.com/repos/",
            "https://github.com/",
        ).replace("/pulls/", "/pull/")

    if subject_type in ("Issue", "Discussion"):
        return url.replace(
            "https://api.github.com/repos/",
            "https://github.com/",
        )

    if subject_type == "Release":
        html_url = notification["repository"]["html_url"]
        return f"{html_url}/releases"

    return url


def main() -> None:
    notifications = fetch_data()
    if notifications is not None:
        print(f"GitHub: {len(notifications)}")
        print("---")
        for notification in notifications:
            subject = notification["subject"]
            subject_type = subject["type"]
            title = subject["title"]
            full_name = notification["repository"]["full_name"]
            url = get_web_url(notification)
            print(f"[{subject_type}] {full_name} {title} | href={url}")
        print("---")
    print(f"Web UI... | href={WEB_URL}")


if __name__ == "__main__":
    main()
