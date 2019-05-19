import json
import gdax
from functools import lru_cache
from websocket import create_connection
from ..config import ExchangeConfig
from ..define import EXCHANGE_MARKET_DATA_ENDPOINT
from ..enums import ExchangeType, OrderType, OrderSubType, PairType, TickType, ChangeReason, TradingType
from ..exchange import Exchange
from ..logging import LOG as log
from ..structs import MarketData, Instrument
from ..utils import parse_date, str_to_currency_pair_type, str_to_side, str_to_order_type, get_keys_from_environment
from .order_entry import CCXTOrderEntryMixin
from .websockets import WebsocketMixin


class KrakenWebsocketMixin(WebsocketMixin):
    @lru_cache(None)
    def subscription(self):
        return [json.dumps({
            "event": "subscribe",
            "pair": [
                [self.currencyPairToString(x) for x in self.options().currency_pairs]
            ],
            "subscription": {
                "name": "ticker"
            }
        })]

    @lru_cache(None)
    def heartbeat(self):
        return ''

    def tickToData(self, jsn: dict) -> MarketData:
        raise NotImplementedError()

    def strToTradeType(self, s: str) -> TickType:
        raise NotImplementedError()

    def tradeReqToParams(self, req) -> dict:
        raise NotImplementedError()

    def currencyPairToString(self, cur: PairType) -> str:
        return cur.value[0].value + '/' + cur.value[1].value

    def orderTypeToString(self, typ: OrderType) -> str:
        raise NotImplementedError()


class KrakenExchange(KrakenWebsocketMixin, CCXTOrderEntryMixin, Exchange):
    def __init__(self, exchange_type: ExchangeType, options: ExchangeConfig) -> None:
        super(KrakenExchange, self).__init__(exchange_type, options)
        self._last = None
        self._orders = {}
