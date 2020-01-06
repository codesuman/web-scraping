import requests
import json

def getData(req_url):
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'app_client': 'consumer_web'
    }

    response = requests.get(req_url, headers=headers)

    return json.loads(
        response.text)  # json.loads - takes a JSON string and convert it back to a dictionary structure