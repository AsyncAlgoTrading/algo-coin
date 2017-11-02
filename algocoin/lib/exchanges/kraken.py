from ..config import ExchangeConfig
from ..enums import ExchangeType
from ..exchange import Exchange
from ..structs import TradeRequest, TradeResponse
from .helpers import KrakenHelpersMixin


class KrakenExchange(KrakenHelpersMixin, Exchange):
    def __init__(self, options: ExchangeConfig) -> None:
        super(KrakenExchange, self).__init__(options)
        self._type = ExchangeType.KRAKEN

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
