"""
An example when you need to change proxy
https://github.com/adw0rd/instagrapi/discussions/299
"""
import json
import random
from urllib.request import urlopen

import requests

from requests.exceptions import ProxyError
from urllib3.exceptions import HTTPError

from instagrapi.exceptions import (
    ClientConnectionError,
    ClientForbiddenError,
    ClientLoginRequired,
    ClientThrottledError,
    GenericRequestError,
    PleaseWaitFewMinutes,
    RateLimitError,
    SentryBlock,
)

PROXY_LIST = []

def load_random_proxy():
    global PROXY_LIST

    if not PROXY_LIST:
        proxy_file_url = 'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data-with-geolocation.json'
        f = urlopen(proxy_file_url)
        proxies = json.loads(f.read())
        PROXY_LIST = [proxy for proxy in proxies if proxy["geolocation"]["country"] == "Germany"]

    timeout = True
    while timeout:
        random_proxy = random.choice(PROXY_LIST)
        try:
            url = f'http://{random_proxy["ip"]}:{random_proxy["port"]}'
            requests.get("https://google.de", timeout=0.5, proxies={"https": url})
            timeout = False
        except Exception as e:
            print(f"Error connecting to proxy {url} ({str(e)})")
        print(f"Using {url}...\n\n")

    return random_proxy


def next_proxy():
    proxy = load_random_proxy()
    return f"http://{proxy['ip']}:{proxy['port']}"



try:
except (ProxyError, HTTPError, GenericRequestError, ClientConnectionError):
    # Network level
    print("Network limit")
    cl.set_proxy(next_proxy())
except (SentryBlock, RateLimitError, ClientThrottledError):
    # Instagram limit level
    print("Ista limit")
    cl.set_proxy(next_proxy())
except (ClientLoginRequired, PleaseWaitFewMinutes, ClientForbiddenError):
    # Logical level
    print("Logical limit")
    cl.set_proxy(next_proxy())

from instagrapi import Client
cl = Client()
cl.login("aug_fil", "...")
cl.photo_upload_to_story(
    path="img.jpg",
    caption="Hi there 🥳"
)