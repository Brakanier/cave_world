import requests
import json

TRACK_URL = 'https://www.google-analytics.com/collect'


def get_data(message):
    data = {
        "command": message,
    }
    return data


def track(user_id, stat):

    r = requests.post(
        TRACK_URL,
        params={
            "v": "1",
            "tid": "UA-100938979-2",
            "cid": user_id,
            "t": "event",
            "ec": stat['category'],
            "ea": stat['action'],
            "el": stat['label'],
            "ev": stat['value']
        },
        headers={'Content-type': 'application/json'},
    )
    print(r)
    # print(json.loads(r.text))


actions_labels = {
    'help': 'Помощь',
}