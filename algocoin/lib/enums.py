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
    EXIT = 9
    HEARTBEAT = 10


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
    COINBASE = 11
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
    BCH = 4
    ZEC = 5


class PairType(BaseEnum):
    # USD Pairs
    USDBTC = (CurrencyType.USD, CurrencyType.BTC)
    USDETH = (CurrencyType.USD, CurrencyType.ETH)
    USDLTC = (CurrencyType.USD, CurrencyType.LTC)
    USDBCH = (CurrencyType.USD, CurrencyType.BCH)
    USDZEC = (CurrencyType.USD, CurrencyType.ZEC)

    # BTC Pairs
    BTCUSD = (CurrencyType.BTC, CurrencyType.USD)
    BTCETH = (CurrencyType.BTC, CurrencyType.ETH)
    BTCLTC = (CurrencyType.BTC, CurrencyType.LTC)
    BTCBCH = (CurrencyType.BTC, CurrencyType.BCH)
    BTCZEC = (CurrencyType.BTC, CurrencyType.ZEC)

    # ETH Pairs
    ETHUSD = (CurrencyType.ETH, CurrencyType.USD)
    ETHBTC = (CurrencyType.ETH, CurrencyType.BTC)

    # LTC Pairs
    LTCUSD = (CurrencyType.LTC, CurrencyType.USD)
    LTCBTC = (CurrencyType.LTC, CurrencyType.BTC)

    # BCH Pairs
    BCHUSD = (CurrencyType.BCH, CurrencyType.USD)
    BCHBTC = (CurrencyType.BCH, CurrencyType.BTC)

    # ZEC Pairs
    ZECUSD = (CurrencyType.ZEC, CurrencyType.USD)
    ZECBTC = (CurrencyType.ZEC, CurrencyType.BTC)
    ZECETH = (CurrencyType.ZEC, CurrencyType.ETH)  # Gemini


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


class TradeResult(BaseEnum):
    NONE = 0
    PENDING = 1
    PARTIAL = 2
    FILLED = 3
    REJECTED = 4
