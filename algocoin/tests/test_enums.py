class TestEnums:
    def setup(self):
        pass
        # setup() before each test method

    def teardown(self):
        pass
        # teardown() after each test method

    @classmethod
    def setup_class(cls):
        pass
        # setup_class() before any methods in this class

    @classmethod
    def teardown_class(cls):
        pass
        # teardown_class() after any methods in this class

    def test_trading_type(self):
        from ..lib.enums import TradingType
        t0 = TradingType.SANDBOX
        t1 = TradingType.LIVE
        t2 = TradingType.BACKTEST
        assert t0 == TradingType.SANDBOX
        assert t1 == TradingType.LIVE
        assert t2 == TradingType.BACKTEST
        assert t0 == TradingType(0)
        assert t1 == TradingType(1)
        assert t2 == TradingType(2)

    def test_exchange_type(self):
        from ..lib.enums import ExchangeType
        t0 = ExchangeType.BITSTAMP
        t1 = ExchangeType.BITFINEX
        t2 = ExchangeType.CEX
        t3 = ExchangeType.GDAX
        t4 = ExchangeType.GEMINI
        t5 = ExchangeType.HITBTC
        t6 = ExchangeType.ITBIT
        t7 = ExchangeType.KRAKEN
        t8 = ExchangeType.LAKE
        t9 = ExchangeType.POLONIEX
        assert t0 == ExchangeType.BITSTAMP
        assert t1 == ExchangeType.BITFINEX
        assert t2 == ExchangeType.CEX
        assert t3 == ExchangeType.GDAX
        assert t4 == ExchangeType.GEMINI
        assert t5 == ExchangeType.HITBTC
        assert t6 == ExchangeType.ITBIT
        assert t7 == ExchangeType.KRAKEN
        assert t8 == ExchangeType.LAKE
        assert t9 == ExchangeType.POLONIEX
        assert t0 == ExchangeType(0)
        assert t1 == ExchangeType(1)
        assert t2 == ExchangeType(2)
        assert t3 == ExchangeType(3)
        assert t4 == ExchangeType(4)
        assert t5 == ExchangeType(5)
        assert t6 == ExchangeType(6)
        assert t7 == ExchangeType(7)
        assert t8 == ExchangeType(8)
        assert t9 == ExchangeType(9)

    def test_currency_type(self):
        from ..lib.enums import CurrencyType
        t0 = CurrencyType.USD
        t1 = CurrencyType.BTC
        t2 = CurrencyType.ETH
        t3 = CurrencyType.LTC
        assert t0 == CurrencyType.USD
        assert t1 == CurrencyType.BTC
        assert t2 == CurrencyType.ETH
        assert t3 == CurrencyType.LTC
        assert t0 == CurrencyType(0)
        assert t1 == CurrencyType(1)
        assert t2 == CurrencyType(2)
        assert t3 == CurrencyType(3)

    def test_side(self):
        from ..lib.enums import Side
        t0 = Side.NONE
        t1 = Side.BUY
        t2 = Side.SELL
        assert t0 == Side.NONE
        assert t1 == Side.BUY
        assert t2 == Side.SELL
        assert t0 == Side(0)
        assert t1 == Side(1)
        assert t2 == Side(2)

    def test_order_type(self):
        from ..lib.enums import OrderType
        t0 = OrderType.NONE
        t1 = OrderType.MARKET
        t2 = OrderType.LIMIT
        assert t0 == OrderType.NONE
        assert t1 == OrderType.MARKET
        assert t2 == OrderType.LIMIT
        assert t0 == OrderType(0)
        assert t1 == OrderType(1)
        assert t2 == OrderType(2)

    def test_order_sub_type(self):
        from ..lib.enums import OrderSubType
        t0 = OrderSubType.NONE
        t1 = OrderSubType.POST_ONLY
        t2 = OrderSubType.FILL_OR_KILL
        # t3 = OrderSubType.ALL_OR_NOTHING
        assert t0 == OrderSubType.NONE
        assert t1 == OrderSubType.POST_ONLY
        assert t2 == OrderSubType.FILL_OR_KILL
        # assert t3 == OrderSubType.ALL_OR_NOTHING
        assert t0 == OrderSubType(0)
        assert t1 == OrderSubType(1)
        assert t2 == OrderSubType(2)
        # assert t3 == OrderSubType(3)
