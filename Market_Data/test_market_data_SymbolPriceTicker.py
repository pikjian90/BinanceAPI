from decimal import Decimal

import pytest
import requests


testdata = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "APTUSDT", "LTCUSDT", "DASHUSDT","SOLUSDT", "OPUSDT", "APEUSDT"]


@pytest.mark.parametrize('symbol', testdata)
def test_market_data_SymbolPriceTicker_valid_symbol(symbol):
    query = {'symbol': symbol}
    response = requests.get('https://api.binance.com/api/v3/ticker/price', params=query)
    resJson = response.json()
    assert resJson['symbol'] == symbol
    assert Decimal(resJson['price']) > 0


def test_market_data_SymbolPriceTicker_missing_symbol():
    response = requests.get('https://api.binance.com/api/v3/ticker/price')
    resJson = response.json()
    assert len(resJson) > 1


def test_market_data_SymbolPriceTicker_empty_symbol():
    query = {'symbol': ''}
    response = requests.get('https://api.binance.com/api/v3/ticker/price', params=query)
    resJson = response.json()
    assert resJson['code'] == -1105
    assert resJson['msg'] == "Parameter 'symbol' was empty."


def test_market_data_SymbolPriceTicker_invalid_symbol():
    query = {'symbol': 'XXX'}
    response = requests.get('https://api.binance.com/api/v3/ticker/price', params=query)
    resJson = response.json()
    assert resJson['code'] == -1121
    assert resJson['msg'] == "Invalid symbol."
