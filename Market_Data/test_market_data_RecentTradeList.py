import time
from decimal import Decimal

import pytest
import requests


testdata = [["BTCUSDT", 10], ["ETHUSDT", 10], ["BNBUSDT", 10], ["APTUSDT", 10],
            ["LTCUSDT", 10], ["DASHUSDT", 10], ["SOLUSDT", 10], ["OPUSDT", 10], ["APEUSDT", 10]]

@pytest.mark.parametrize('symbol, recent_trade_limit', testdata)
def test_market_data_RecentTradeList_valid_symbol_limit(symbol, recent_trade_limit):
    query = {'symbol': symbol, 'limit': recent_trade_limit}
    response = requests.get('https://api.binance.com/api/v3/trades', params=query)
    resJson = response.json()
    assert len(resJson) == recent_trade_limit
    assert Decimal(resJson[0]['price']) > 0
    assert Decimal(resJson[0]['qty']) > 0
    assert Decimal(resJson[0]['quoteQty']) > 0

    recent_trade_time = resJson[0]['time']
    current_time = str(time.time()).replace(".", "")
    assert int(recent_trade_time) < int(current_time[0:13])
    assert resJson[0]['isBuyerMaker'] is True or resJson[0]['isBuyerMaker'] is False
    assert resJson[0]['isBestMatch'] is True or resJson[0]['isBestMatch'] is False


def test_market_data_RecentTradeList_default_limit():
    query = {'symbol': 'BTCUSDT'}
    response = requests.get('https://api.binance.com/api/v3/trades', params=query)
    resJson = response.json()
    assert len(resJson) == 500
    assert len(resJson) == 500


def test_market_data_RecentTradeList_empty_symbol():
    query = {'symbol': ''}
    response = requests.get('https://api.binance.com/api/v3/trades', params=query)
    resJson = response.json()
    assert resJson['code'] == -1105
    assert resJson['msg'] == "Parameter 'symbol' was empty."


def test_market_data_RecentTradeList_invalid_symbol():
    query = {'symbol': 'XXX'}
    response = requests.get('https://api.binance.com/api/v3/trades', params=query)
    resJson = response.json()
    assert resJson['code'] == -1121
    assert resJson['msg'] == "Invalid symbol."


def test_market_data_RecentTradeList_missing_symbol():
    response = requests.get('https://api.binance.com/api/v3/trades')
    resJson = response.json()
    assert resJson['code'] == -1102
    assert resJson['msg'] == "Mandatory parameter 'symbol' was not sent, was empty/null, or malformed."
