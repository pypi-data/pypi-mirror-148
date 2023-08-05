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
    response = r.get(url=url, data=data, headers=headers)

    content = response.json()
    results = []
    if data["limit"]:
        for i in range(data['limit']):
            results.append(content[i])
            


    return response, results, response.status_code