from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def members(cls):
        return cls.__members__.keys()


class TickType(BaseEnum):
    TRADE = 'TRADE'
    RECEIVED = 'RECEIVED'
    OPEN = 'OPEN'
    DONE = 'DONE'
    CHANGE = 'CHANGE'
    ERROR = 'ERROR'
    ANALYZE = 'ANALYZE'
    HALT = 'HALT'
    CONTINUE = 'CONTINUE'
    EXIT = 'EXIT'
    HEARTBEAT = 'HEARTBEAT'


class TradingType(BaseEnum):
    NONE = 'NONE'
    SANDBOX = 'SANDBOX'
    LIVE = 'LIVE'
    BACKTEST = 'BACKTEST'
    SIMULATION = 'SIMULATION'


class ExchangeType(BaseEnum):
    NONE = 'NONE'
    BITSTAMP = 'BITSTAMP'
    BITFINEX = 'BITFINEX'
    CEX = 'CEX'
    GDAX = 'GDAX'
    COINBASE = 'COINBASE'
    GEMINI = 'GEMINI'
    HITBTC = 'HITBTC'
    ITBIT = 'ITBIT'
    KRAKEN = 'KRAKEN'
    LAKE = 'LAKE'
    POLONIEX = 'POLONIEX'


class CurrencyType(BaseEnum):
    USD = 'USD'
    BTC = 'BTC'
    ETH = 'ETH'
    LTC = 'LTC'
    BCH = 'BCH'
    ZEC = 'ZEC'


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

    @staticmethod
    def from_string(str):
        s1 = str[:3]
        c1 = CurrencyType(s1)
        s2 = str[3:6]
        c2 = CurrencyType(s2)
        return PairType((c1, c2))


class Side(BaseEnum):
    NONE = 'NONE'
    BUY = 'BUY'
    SELL = 'SELL'


class OrderType(BaseEnum):
    NONE = 'NONE'
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'


class OrderSubType(BaseEnum):
    NONE = 'NONE'
    POST_ONLY = 'POST_ONLY'
    FILL_OR_KILL = 'FILL_OR_KILL'
    # ALL_OR_NOTHING = 3


class TradeResult(BaseEnum):
    NONE = 'NONE'
    PENDING = 'PENDING'
    PARTIAL = 'PARTIAL'
    FILLED = 'FILLED'
    REJECTED = 'REJECTED'
