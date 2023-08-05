import requests as r
import json

def make_request(api_key, url, config=None):
    if config == None:
        data = {
            "apiKey": api_key
        }
    else:
        data = config
        data["apiKey"] = api_key
    headers = {
        "X-Api-Key": api_key
    }
    print(data)
    response = r.get(url=url, data=data, headers=headers)

    return response, response.json(), response.status_code