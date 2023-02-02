from decimal import Decimal
import pytest
import requests

testdata = [["BTCUSDT", 200], ["ETHUSDT", 200], ["BNBUSDT", 200], ["APTUSDT", 200],
            ["LTCUSDT", 200], ["DASHUSDT", 200], ["SOLUSDT", 200], ["OPUSDT", 200], ["APEUSDT", 200]]


@pytest.mark.parametrize('symbol, limit', testdata)
def test_market_data_OrderBook_valid_symbol_limit(symbol, limit):
    query = {'symbol': symbol, 'limit': limit}
    response = requests.get('https://api.binance.com/api/v3/depth', params=query)
    resJson = response.json()
    assert len(resJson['bids']) == limit
    assert Decimal(resJson['bids'][0][0]) > 0
    assert Decimal(resJson['bids'][0][1]) > 0
    assert len(resJson['asks']) == limit
    assert Decimal(resJson['asks'][0][0]) > 0
    assert Decimal(resJson['asks'][0][1]) > 0


def test_market_data_OrderBook_default_limit():
    query = {'symbol': 'BTCUSDT'}
    response = requests.get('https://api.binance.com/api/v3/depth', params=query)
    resJson = response.json()
    assert len(resJson['bids']) == 100
    assert len(resJson['asks']) == 100


def test_market_data_OrderBook_empty_symbol():
    query = {'symbol': ''}
    response = requests.get('https://api.binance.com/api/v3/depth', params=query)
    resJson = response.json()
    assert resJson['code'] == -1105
    assert resJson['msg'] == "Parameter 'symbol' was empty."


def test_market_data_OrderBook_invalid_symbol():
    query = {'symbol': 'XXX'}
    response = requests.get('https://api.binance.com/api/v3/depth', params=query)
    resJson = response.json()
    assert resJson['code'] == -1121
    assert resJson['msg'] == "Invalid symbol."


def test_market_data_OrderBook_missing_symbol():
    response = requests.get('https://api.binance.com/api/v3/depth')
    resJson = response.json()
    assert resJson['code'] == -1102
    assert resJson['msg'] == "Mandatory parameter 'symbol' was not sent, was empty/null, or malformed."
