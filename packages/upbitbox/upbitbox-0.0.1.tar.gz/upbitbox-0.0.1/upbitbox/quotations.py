__all__ = [ "request", "markets", "candles", "orderbook" ]

import pandas as pd
from . import request_api

def request(URL, **kwargs):
    """ Common requester """
    headers = { "Accept": "application/json" }
    return request_api.public_get(URL, headers=headers, **kwargs)


def markets(is_detail:bool=False) -> pd.DataFrame:
    """ get list of tradeable market on Upbit
    :param is_detail (bool): Include markets to watch out for as details.
    """
    URL = f"https://api.upbit.com/v1/market/all"
    data = request(URL, isDetail=is_detail)

    return pd.DataFrame(data)


def candles(unit:int, market:str, to:str=None, count:int=None) -> pd.DataFrame: 
    """ get candles on Upbit
    :param unit (int): minute unit, (possible value: 1, 3, 5, 15, 10, 30, 60, 240)
    :param market (str): market code, (ex. KRW-BTC)
    :param to (str): last candle time, (format: yyyy-mm-dd HH:mm:ss)
    :param count (int): candle count, (max: 200)
    """
    URL = f"https://api.upbit.com/v1/candles/minutes/{unit}"
    data = request(URL, market=market, to=to, count=count)

    return pd.DataFrame(data)


def orderbook(markets) -> pd.DataFrame:
    """ get ask & bid prices on Upbit
    :param markets (str): market codes, (ex. KRW-BTC, BTC-ETH)
    """
    URL = f"https://api.upbit.com/v1/orderbook"
    data = request(URL, markets=markets)

    return pd.DataFrame(data)