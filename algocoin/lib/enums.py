from enum import Enum


class TickType(Enum):
    MATCH = 0
    RECEIVED = 1
    ERROR = 2
    OPEN = 3
    DONE = 4
    CHANGE = 5
    ANALYZE = 6
    HALT = 7
    CONTINUE = 8


class TradingType(Enum):
    SANDBOX = 0
    LIVE = 1
    BACKTEST = 2


class ExchangeType(Enum):
    BITSTAMP = 0
    BITFINEX = 1
    BTCC = 2
    CEX = 3
    GDAX = 4
    GEMINI = 5
    HITBTC = 6
    POLONIEX = 7


class CurrencyType(Enum):
    USD = 0
    BTC = 1
    ETH = 2
    LTC = 3


class Side(Enum):
    BUY = 0
    SELL = 1


class OrderType(Enum):
    MARKET = 0
    LIMIT = 1


class OrderSubType(Enum):
    NONE = 0
    POST_ONLY = 1
    FILL_OR_KILL = 2
    # ALL_OR_NOTHING = 3
