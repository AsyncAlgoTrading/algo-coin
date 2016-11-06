from enum import Enum


class TradingType(Enum):
    SANDBOX = 1
    LIVE = 2
    BACKTEST = 3


class ExchangeType(Enum):
    BITSTAMP = 1
    BITFINEX = 2
    BTCC = 3
    CEX = 4
    GDAX = 5
    GEMINI = 6
    HITBTC = 7
    POLONIEX = 8


class CurrencyType(Enum):
    USD = 0
    BTC = 1
    ETH = 2
    LTC = 3
