from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def members(cls):
        return cls.__members__.keys()


class TickType(BaseEnum):
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


class TradingType(BaseEnum):
    NONE = 0
    SANDBOX = 1
    LIVE = 2
    BACKTEST = 3


class ExchangeType(BaseEnum):
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


class CurrencyType(BaseEnum):
    USD = 0
    BTC = 1
    ETH = 2
    LTC = 3


class Side(BaseEnum):
    NONE = 0
    BUY = 1
    SELL = 2


class OrderType(BaseEnum):
    NONE = 0
    MARKET = 1
    LIMIT = 2


class OrderSubType(BaseEnum):
    NONE = 0
    POST_ONLY = 1
    FILL_OR_KILL = 2
    # ALL_OR_NOTHING = 3
