import requests


def test_market_data_ServerTime():
    response = requests.get('https://api.binance.com/api/v3/time')
    resJson = response.json()
    serverTime = resJson['serverTime']
    assert serverTime > 0
