from ..config import ExchangeConfig
from ..enums import ExchangeType
from ..exchange import Exchange
from ..structs import TradeRequest, TradeResponse
from .helpers import ItBitHelpersMixin


class DeribitExchange(ItBitHelpersMixin, Exchange):
    def __init__(self, options: ExchangeConfig) -> None:
        super(DeribitExchange, self).__init__(options)
        self._type = ExchangeType.ITBIT

    def run(self, engine) -> None:
        pass

    def accounts(self) -> list:
        return self._accounts

    def orderBook(self, level=1):
        '''get order book'''
        return self._client.getProductOrderBook(level=level)

    def buy(self, req: TradeRequest) -> TradeResponse:
        '''execute a buy order'''

    def sell(self, req: TradeRequest) -> TradeResponse:
        '''execute a sell order'''
