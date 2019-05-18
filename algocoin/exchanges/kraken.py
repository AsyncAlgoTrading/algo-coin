import json
import gdax
from functools import lru_cache
from websocket import create_connection
from ..config import ExchangeConfig
from ..define import EXCHANGE_MARKET_DATA_ENDPOINT
from ..enums import OrderType, OrderSubType, PairType, TickType, ChangeReason, TradingType
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
                [KrakenWebsocketMixin.currencyPairToString(x) for x in self.options().currency_pairs]
            ],
            "subscription": {
                "name": "ticker"
            }
        })]

    @lru_cache(None)
    def heartbeat(self):
        return ''

    def close(self):
        '''close the websocket'''

    def seqnum(self, number: int):
        '''manage sequence numbers'''

    def run(self, engine) -> None:
        # DEBUG
        options = self.options()

        while True:
            # startup and redundancy
            log.info('Starting....')
            self.ws = create_connection(EXCHANGE_MARKET_DATA_ENDPOINT(options.exchange_type, options.trading_type))
            log.info('Connected!')

            for sub in self.subscription():
                self.ws.send(sub)
                log.info('Sending Subscription %s' % sub)

            self.ws.send(self.heartbeat())
            log.info('Sending Heartbeat %s' % self.heartbeat())

            log.info('')
            log.info('Starting algo trading')
            try:
                while True:
                    self.receive()

            except KeyboardInterrupt:
                log.critical('Terminating program')
                return

    @staticmethod
    def tickToData(jsn: dict) -> MarketData:
        raise NotImplementedError()

    @staticmethod
    def strToTradeType(s: str) -> TickType:
        raise NotImplementedError()

    @staticmethod
    def tradeReqToParams(req) -> dict:
        raise NotImplementedError()

    @staticmethod
    def currencyPairToString(cur: PairType) -> str:
        return cur.value[0].value + '/' + cur.value[1].value

    @staticmethod
    def orderTypeToString(typ: OrderType) -> str:
        raise NotImplementedError()


class KrakenExchange(KrakenWebsocketMixin, CCXTOrderEntryMixin, Exchange):
    def __init__(self, options: ExchangeConfig) -> None:
        super(KrakenExchange, self).__init__(options)
        self._last = None
        self._orders = {}
