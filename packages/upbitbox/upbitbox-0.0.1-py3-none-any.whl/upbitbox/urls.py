__all__ = [ 'url' ]

from collections import namedtuple

_urls = {
    # Exchange.
    'accounts': 'https://api.upbit.com/v1/accounts',

    # Quotation.
    'markets': 'https://api.upbit.com/v1/market/all',
    'candles': 'https://api.upbit.com/v1/candles/minutes',
    'orderbook': 'https://api.upbit.com/v1/orderbook',
}


def to_object(name, data):
    _th_ = namedtuple(name, data.keys())
    return _th_(**data)


url = to_object('urls', _urls)
