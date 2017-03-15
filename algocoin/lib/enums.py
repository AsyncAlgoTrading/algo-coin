from enum import Enum


class TickType(Enum):
    TRADE = 0
    RECEIVED = 1
    OPEN = 2
    DONE = 3
    CHANGE = 4
    ERROR = 5

    ANALYZE = 6

    HALT = 7
    CONTINUE = 8

    HEARTBEAT = 9


class TradingType(Enum):
    NONE = 0
    SANDBOX = 1
    LIVE = 2
    BACKTEST = 3


class ExchangeType(Enum):
    NONE = 0
    BITSTAMP = 1
    BITFINEX = 2
    CEX = 3
    GDAX = 4
    GEMINI = 5
    HITBTC = 6
    ITBIT = 7
    KRAKEN = 8
    LAKE = 9
    POLONIEX = 10


class CurrencyType(Enum):
    USD = 0
    BTC = 1
    ETH = 2
    LTC = 3


def strToCurrencyType(s: str) -> CurrencyType:
    s = s.upper()
    if 'BTC' in s:
        return CurrencyType.BTC
    if 'ETH' in s:
        return CurrencyType.ETH
    if 'LTC' in s:
        return CurrencyType.LTC
    return CurrencyType.USD


class Side(Enum):
    NONE = 0
    BUY = 1
    SELL = 2


def strToSide(s: str) -> Side:
    s = s.upper()
    if 'BUY' in s or 'BID' in s:
        return Side.BUY
    if 'SELL' in s or 'ASK' in s:
        return Side.SELL
    return Side.NONE


class OrderType(Enum):
    NONE = 0
    MARKET = 1
    LIMIT = 2


def strToOrderType(s: str) -> OrderType:
    s = s.upper()
    if 'MARKET' in s:
        return OrderType.MARKET
    if 'LIMIT' in s:
        return OrderType.LIMIT
    return OrderType.NONE


class OrderSubType(Enum):
    NONE = 0
    POST_ONLY = 1
    FILL_OR_KILL = 2
    # ALL_OR_NOTHING = 3
