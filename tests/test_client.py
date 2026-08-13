import requests

url = 'http://localhost:2702/get'

def test_http_round_true():
    params = {
        'year': 2013,
        'month': 5,
        'day': 31,
        'hour_utc': 12,
        'station': 72357,
        'is_round': True
    }

    response = requests.get(url, params=params)
    assert response.status_code == 200

