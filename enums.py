from enum import Enum


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
    FILL_OR_KILL = 0
    ALL_OR_NOTHING = 1
