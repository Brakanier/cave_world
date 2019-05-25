
def track(user_id, stat):
    import requests
    track_url = 'https://www.google-analytics.com/collect'
    r = requests.post(
        track_url,
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

