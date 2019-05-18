import json
from abc import abstractstaticmethod
from datetime import datetime
from functools import lru_cache
from websocket import create_connection
from ..data_source import StreamingDataSource
from ..define import EXCHANGE_MARKET_DATA_ENDPOINT
from ..enums import OrderType, OrderSubType, Side, PairType, CurrencyType, TickType, ChangeReason
from ..utils import parse_date, str_to_currency_pair_type, str_to_side, str_to_order_type
from ..structs import MarketData, Instrument
from ..logging import LOG as log


def exchange_type_to_websocket_client(exchange_type):
    if exchange_type == ExchangeType.COINBASE:
        return CoinbaseWebsocketMixin
    raise Exception(f'No websocket client for {exchange_type}')


class WebsocketMixin(StreamingDataSource):
    def seqnum(self, number: int):
        '''manage sequence numbers'''

    @abstractstaticmethod
    def tickToData(jsn: dict) -> MarketData:
        pass

    @abstractstaticmethod
    def strToTradeType(s: str) -> TickType:
        pass

    @abstractstaticmethod
    def tradeReqToParams(req) -> dict:
        pass

    @staticmethod
    def currencyToString(cur: CurrencyType) -> str:
        if cur == CurrencyType.BTC:
            return 'BTC'
        if cur == CurrencyType.ETH:
            return 'ETH'
        if cur == CurrencyType.LTC:
            return 'LTC'
        if cur == CurrencyType.BCH:
            return 'BCH'
        else:
            raise Exception('Pair not recognized: %s' % str(cur))

    @abstractstaticmethod
    def currencyPairToString(cur: PairType) -> str:
        pass

    @abstractstaticmethod
    def orderTypeToString(typ: OrderType) -> str:
        pass

    def reasonToTradeType(s: str) -> TickType:
        pass
