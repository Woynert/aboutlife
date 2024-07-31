#!/usr/bin/env python3

import urllib.parse
import requests
import sys


def printerr(message):
    print(message, file=sys.stderr)


def fetch_pages(host: str, uri: str = "/", params: dict = {}):
    try:
        params_encoded = urllib.parse.urlencode(params)
        complete_url = f"https://{host}/{uri}?{params_encoded}"
        printerr(f"Trying {complete_url} ...")

        response = requests.get(complete_url, params=params)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
    except Exception as e:
        printerr(e)
    return None


# check all args are provided

if len(sys.argv) < 3:
    print(
        f"""Usage:
{sys.argv[0]} [access_key] [collection_id]
Example:
{sys.argv[0]} XXXXXXXXXXXX 5044222 > images.txt"""
    )
    exit(1)

# get args

api_key: str = sys.argv[1]
collection_id: int = int(sys.argv[2])

# build query url

page = 1
params = {"client_id": api_key, "page": page, "per_page": 30, "orientation": "portrait"}
UNSPLASH_HOST: str = "api.unsplash.com"
query_uri: str = f"/collections/{collection_id}/photos"

# query it

images = fetch_pages(UNSPLASH_HOST, query_uri, params) or []
while len(images):
    params["page"] = page
    for image in images:
        regular_url = image["urls"]["regular"]
        regular_url = regular_url.split("?")[0]
        print(regular_url)

    # try next page
    page += 1
    images = fetch_pages(UNSPLASH_HOST, query_uri, params) or []

printerr(f"Made ({page}) requests")
