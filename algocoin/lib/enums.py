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
    HEARTBEAT = 9


class TradingType(Enum):
    SANDBOX = 0
    LIVE = 1
    BACKTEST = 2


class ExchangeType(Enum):
    BITSTAMP = 0
    BITFINEX = 1
    CEX = 2
    GDAX = 3
    GEMINI = 4
    HITBTC = 5
    ITBIT = 6
    KRAKEN = 7
    LAKE = 8
    POLONIEX = 9


class CurrencyType(Enum):
    USD = 0
    BTC = 1
    ETH = 2
    LTC = 3


def strToCurrencyType(s):
    s = s.upper()
    if 'BTC' in s:
        return CurrencyType.BTC
    if 'ETH' in s:
        return CurrencyType.ETH
    if 'LTC' in s:
        return CurrencyType.LTC
    return CurrencyType.USD


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
