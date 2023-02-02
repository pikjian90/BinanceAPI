import requests


def test_market_data_Ping():
    response = requests.get('https://api.binance.com/api/v3/ping')
    assert response.reason == 'OK'
    assert response.status_code == 200
