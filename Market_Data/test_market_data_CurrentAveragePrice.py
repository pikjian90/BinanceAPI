from decimal import Decimal

import pytest
import requests

testdata = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "APTUSDT", "LTCUSDT", "DASHUSDT","SOLUSDT", "OPUSDT", "APEUSDT"]


@pytest.mark.parametrize('symbol', testdata)
def test_market_data_CurrentAveragePrice_valid_symbol(symbol):
    query = {'symbol': symbol}
    response = requests.get('https://api.binance.com/api/v3/avgPrice', params=query)
    resJson = response.json()
    assert resJson['mins'] > 0
    assert Decimal(resJson['price']) > 0


def test_market_data_CurrentAveragePrice_empty_symbol():
    query = {'symbol': ''}
    response = requests.get('https://api.binance.com/api/v3/avgPrice', params=query)
    resJson = response.json()
    assert resJson['code'] == -1105
    assert resJson['msg'] == "Parameter 'symbol' was empty."


def test_market_data_CurrentAveragePrice_invalid_symbol():
    query = {'symbol': 'XXX'}
    response = requests.get('https://api.binance.com/api/v3/avgPrice', params=query)
    resJson = response.json()
    assert resJson['code'] == -1121
    assert resJson['msg'] == "Invalid symbol."


def test_market_data_CurrentAveragePrice_missing_symbol():
    response = requests.get('https://api.binance.com/api/v3/avgPrice')
    resJson = response.json()
    assert resJson['code'] == -1102
    assert resJson['msg'] == "Mandatory parameter 'symbol' was not sent, was empty/null, or malformed."
