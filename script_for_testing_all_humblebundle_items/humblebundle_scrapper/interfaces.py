import json

import requests


def download_data(url, parser_func):
    response = requests.get(url)
    raw_data_json = parser_func(response.content)
    return json.loads(raw_data_json)
