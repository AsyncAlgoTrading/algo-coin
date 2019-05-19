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
from .utils.poloniex import POLONIEX_CURRENCY_ID, POLONIEX_PAIR_ID


class PoloniexWebsocketMixin(WebsocketMixin):
    @lru_cache(None)
    def subscription(self):
        return [json.dumps({"command": "subscribe", "channel": "1002"})] + \
                [json.dumps({"command": "subscribe", "channel": POLONIEX_PAIR_ID.get(PoloniexWebsocketMixin.currencyPairToString(x))}) for x in self.options().currency_pairs],  # ticker data

    @lru_cache(None)
    def heartbeat(self):
        return json.dumps({"command": "subscribe", "channel": "1010"})

    def tickToData(self, jsn: dict) -> MarketData:
        raise NotImplementedError()

    def strToTradeType(self, s: str) -> TickType:
        raise NotImplementedError()

    def tradeReqToParams(self, req) -> dict:
        raise NotImplementedError()

    def currencyPairToString(self, cur: PairType) -> str:
        return cur.value[0].value + '_' + cur.value[1].value

    def orderTypeToString(self, typ: OrderType) -> str:
        raise NotImplementedError()


class PoloniexExchange(PoloniexWebsocketMixin, CCXTOrderEntryMixin, Exchange):
    def __init__(self, exchange_type: ExchangeType, options: ExchangeConfig) -> None:
        super(PoloniexExchange, self).__init__(exchange_type, options)
        self._last = None
        self._orders = {}
