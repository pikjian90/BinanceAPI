import pytest
import requests


testdata = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "APTUSDT", "LTCUSDT", "SOLUSDT","SOLUSDT", "UNIUSDT", "APEUSDT"]


@pytest.mark.parametrize('symbol', testdata)
def test_market_data_ExchangeInformation_valid_symbol(symbol):
    query = {'symbol': symbol}
    response = requests.get('https://api.binance.com/api/v3/exchangeInfo', params=query)
    resJson = response.json()
    assert resJson['timezone'] == 'UTC'
    assert resJson['serverTime'] > 0
    assert resJson['symbols'][0]['symbol'] == symbol
    assert resJson['symbols'][0]['status'] == 'TRADING'
    assert resJson['symbols'][0]['baseAsset'] == symbol[0:3]
    assert resJson['symbols'][0]['quoteAsset'] == symbol[3:]
    assert resJson['symbols'][0]['quotePrecision'] == 8
    assert resJson['symbols'][0]['quoteAssetPrecision'] == 8
    assert resJson['symbols'][0]['icebergAllowed'] is True


def test_market_data_ExchangeInformation_empty_symbol():
    query = {'symbol': ''}
    response = requests.get('https://api.binance.com/api/v3/exchangeInfo', params=query)
    resJson = response.json()
    assert resJson['code'] == -1105
    assert resJson['msg'] == "Parameter 'symbol' was empty."


def test_market_data_ExchangeInformation_invalid_symbol():
    query = {'symbol': 'XXX'}
    response = requests.get('https://api.binance.com/api/v3/exchangeInfo', params=query)
    resJson = response.json()
    assert resJson['code'] == -1121
    assert resJson['msg'] == "Invalid symbol."