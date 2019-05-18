import ccxt
from ..config import ExchangeConfig
from ..enums import ExchangeType
from ..exchange import Exchange
from .order_entry import CCXTOrderEntryMixin
from .websockets import CoinbaseWebsocketMixin


def exchange_type_to_ccxt_client(exchange_type: ExchangeType):
    if exchange_type == ExchangeType.GDAX:
        return ccxt.coinbasepro
    elif exchange_type == ExchangeType.GEMINI:
        return ccxt.gemini
    elif exchange_type == ExchangeType.POLONIEX:
        return ccxt.poloniex


class CCXTExchange(CoinbaseWebsocketMixin, CCXTOrderEntryMixin, Exchange):
    def __init__(self, options: ExchangeConfig) -> None:
        super(CCXTExchange, self).__init__(options)
        self._last = None
        self._orders = {}
