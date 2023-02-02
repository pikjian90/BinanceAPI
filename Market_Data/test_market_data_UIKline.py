import time
from decimal import Decimal

import pytest
import requests

testdata = [["BTCUSDT", '1m'], ["BTCUSDT", '15m'], ["BTCUSDT", '1h'], ["BTCUSDT", '1d'], ["BTCUSDT", '1w'],
            ["ETHUSDT", '1m'], ["ETHUSDT", '15m'], ["ETHUSDT", '1h'], ["ETHUSDT", '1d'], ["ETHUSDT", '1w'],
            ["BNBUSDT", '1m'], ["BNBUSDT", '15m'], ["BNBUSDT", '1h'], ["BNBUSDT", '1d'], ["BNBUSDT", '3d']
            ]


@pytest.mark.parametrize('symbol, interval', testdata)
def test_market_data_CurrentAveragePrice_valid_symbol_interval(symbol, interval):
    query = {'symbol': symbol, 'interval': interval}
    response = requests.get('https://api.binance.com/api/v3/uiKlines', params=query)
    resJson = response.json()

    kline_open_time = Decimal(resJson[0][0])
    kline_open_price = Decimal(resJson[0][1])
    kline_high_price = Decimal(resJson[0][2])
    kline_low_price = Decimal(resJson[0][3])
    kline_close_price = Decimal(resJson[0][4])
    kline_volume = Decimal(resJson[0][5])
    kline_close_time = Decimal(resJson[0][6])
    kline_quote_asset_volume = Decimal(resJson[0][7])
    kline_number_of_trades = Decimal(resJson[0][8])
    kline_take_buy_base_asset_volume = Decimal(resJson[0][9])
    kline_take_buy_quote_asset_volume = Decimal(resJson[0][10])
    kline_used_field = resJson[0][11]

    current_time = str(time.time()).replace(".", "")
    assert int(kline_open_time) < int(current_time[0:13])

    assert 1 < kline_open_price < 60000
    assert 1 < kline_high_price < 60000
    assert 1 < kline_low_price < 60000
    assert 1 < kline_close_price < 60000
    assert kline_low_price <= kline_high_price
    assert kline_volume > 0
    assert int(kline_open_time) < int(kline_close_time)
    assert kline_quote_asset_volume > 0
    assert kline_number_of_trades > 0
    assert kline_take_buy_base_asset_volume > 0
    assert kline_take_buy_quote_asset_volume > 0
    assert kline_used_field == '0'


def test_market_data_CurrentAveragePrice_only_symbol():
    query = {'symbol': 'BTCUSDT'}
    response = requests.get('https://api.binance.com/api/v3/uiKlines', params=query)
    resJson = response.json()

    assert resJson['code'] == -1102
    assert resJson['msg'] == "Mandatory parameter 'interval' was not sent, was empty/null, or malformed."


def test_market_data_CurrentAveragePrice_only_inteval():
    query = {'interval': '1m'}
    response = requests.get('https://api.binance.com/api/v3/uiKlines', params=query)
    resJson = response.json()

    assert resJson['code'] == -1102
    assert resJson['msg'] == "Mandatory parameter 'symbol' was not sent, was empty/null, or malformed."


def test_market_data_CurrentAveragePrice_empty_symbol():
    query = {'symbol': '', 'interval': '1m'}
    response = requests.get('https://api.binance.com/api/v3/uiKlines', params=query)
    resJson = response.json()

    assert resJson['code'] == -1105
    assert resJson['msg'] == "Parameter 'symbol' was empty."


def test_market_data_CurrentAveragePrice_empty_interval():
    query = {'symbol': 'BTCUSDT', 'interval': ''}
    response = requests.get('https://api.binance.com/api/v3/klines', params=query)
    resJson = response.json()

    assert resJson['code'] == -1105
    assert resJson['msg'] == "Parameter 'interval' was empty."


def test_market_data_CurrentAveragePrice_invalid_symbol():
    query = {'symbol': 'XXX', 'interval': '1'}
    response = requests.get('https://api.binance.com/api/v3/klines', params=query)
    resJson = response.json()

    assert resJson['code'] == -1121
    assert resJson['msg'] == "Invalid symbol."


def test_market_data_CurrentAveragePrice_invalid_interval():
    query = {'symbol': 'BTCUSDT', 'interval': '1'}
    response = requests.get('https://api.binance.com/api/v3/klines', params=query)
    resJson = response.json()

    assert resJson['code'] == -1120
    assert resJson['msg'] == 'Invalid interval.'


def test_market_data_CurrentAveragePrice_missing_symbol_interval():
    response = requests.get('https://api.binance.com/api/v3/klines')
    resJson = response.json()

    assert resJson['code'] == -1102
    assert resJson['msg'] == "Mandatory parameter 'symbol' was not sent, was empty/null, or malformed."
