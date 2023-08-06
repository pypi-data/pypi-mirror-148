__all__ = [ "create_upbit" ]

r"""
업비트 거래소에서 ``주문``, ``출금``, ``입금`` 그리고 유저의 ``자산``등의 대한 정보를 요청할 수 있습니다.
API신청을 통해 사용권한을 획득할 수 있으며 제공된 ``ACCESS KEY``와 ``SECRET KEY``를 입력하면
원하는 요청을 수행할 수 있습니다.

Example::
    >>> import pyupbit
    >>> handle = pyupbit._UpbitHandler
    >>> print(handle.account())

민감한 데이터의 요청이 진행되기에 유저 키에 대한 관리가 필요합니다. 
"""

import uuid
import jwt
import hashlib
import pandas as pd
from urllib.parse import urlencode

from requests import request

from . import request_api

class _UpbitHandler:
    def __init__(self, access_key:str, secret_key:str) -> None:
        """ Init
        :param access_key (str): `access_key` provided by Upbit
        :param secret_key (str): `secret_key` provided by Upbit
        """
        self.access_key = access_key
        self.secret_key = secret_key

    def get_token(self, query:dict=None):
        """ 토큰 제작
        :param query (dict): 업비트에 맞게 토큰에 들어갈 데이터
        """
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4)
        }

        if query:
            m = hashlib.sha512()
            m.update(urlencode(query, doseq=True).replace("%5B%5D=", "[]=").encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = "SHA512"

        return f"Bearer {jwt.encode(payload, self.secret_key)}"


    def auth(self, headers:dict={}, **kwargs) -> dict:
        """ Request 인증 처리
        :param header (dict): request headers
        :param kwargs (**): request parameter
        """
        headers['Authorization'] = self.get_token(query=kwargs)
        return headers
              

    def send(self, method, URL, **kwargs):
        """ Send Warper """
        headers = self.auth(**kwargs)
        return method(URL, headers=headers, **kwargs)

    #----------------------------------------------------------------
    def accounts(self) -> pd.DataFrame:
        """ Get a list of assets i own. """
        URL = f"https://api.upbit.com/v1/accounts"
        data = self.send(request_api.get, URL)

        return pd.DataFrame(data)


    def chance(self, market:str) -> pd.DataFrame:
        """ Check the order availability information for each market 
        :param market (str): market code, (ex. KRW-BTC)
        """
        URL = "https://api.upbit.com/v1/orders/chance"
        data = self.send(request_api.get, URL, market=market)

        return pd.DataFrame(data)


    def order(self, uuid:str):
        """ get list of order """
        URL = f"https://api.upbit.com/v1/order"
        data = self.send(request_api.get, URL, uuid=uuid,)

        return pd.DataFrame(data)


    def orders(self, market:str, state:str) -> pd.DataFrame:
        """ get list of order 
        :param market (str): market code, (ex. KRW-BTC)
        :param state (str): order state, (`wait`, `watch`, `done`, `cancel`)
        """
        URL = f"https://api.upbit.com/v1/orders"
        data = self.send(request_api.get, URL, markets=market, state=state)

        return pd.DataFrame(data)
    

    def order_coin(self, market:str, price:float, amount:float, side:str, ord_type:str) -> pd.DataFrame:
        """ order coin
        :param market (str): market code, (ex: KRW-BTC)
        :param price (float): order price, (ex: 10000.0)
        :param amount (float): order amount, (ex: 10.0)
        :param side (str): bid(매수), ask(매도)
        :param ord_type (str): 주문 방식 ex) limit(지정가), price(시장가매수), market(시장가매도)
        """
        URL = f"https://api.upbit.com/v1/orders"
        data = self.send(request_api.post, URL, market=market, price=str(price), volume=str(amount), side=side, ord_type=ord_type)

        return pd.DataFrame(data)
    

    def cancel_order(self, uuid:str) -> pd.DataFrame:
        """ Cancel order
        :param uuid (str): order uuid
        """
        URL = "https://api.upbit.com/v1/order"
        data = self.send(request_api.delete, URL, uuid=uuid)

        return pd.DataFrame(data)

    
    def withdraws_krw(self, amount:float) -> pd.DataFrame:
        """ 원화 출금
        :param amount (float): KRW amount 
        """
        URL = f"https://api.upbit.com/v1/withdraws/krw"
        data = self.send(request_api.post, URL, amount=amount)

        return pd.DataFrame(data)

    def withdraws_coin(self, currency:str, amount:float, address:str, secondary_address:str=None, transaction_type:str=None) -> pd.DataFrame:
        """ 코인 출금
        :param currency (str): currency symbol (ex. BTC, ETH, ...)
        :param amount (float): coin amount (ex. 0.001)
        :param address (str): target wallet address 
        :param secondary_address (str): target wallet address + @
        :param transaction_type (str): withdraws type
        """
        ULR = f"https://api.upbit.com/v1/withdraws/coin"
        data = self.send(request_api.post, 
            currency=currency, 
            amount=str(amount), 
            address=address, 
            secondary_address=secondary_address, 
            transaction_type=transaction_type
        )

        return pd.DataFrame(data)

    
    def wallet(self) -> pd.DataFrame:
        """ 입출금 현황 """
        URL = f"https://api.upbit.com/v1/status/wallet"
        data = self.send(request_api.get, URL)

        return pd.DataFrame(data)

    


def create_upbit(access_key, secret_key):
    return _UpbitHandler(access_key, secret_key)
