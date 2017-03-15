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
        t0 = TradingType.NONE
        t1 = TradingType.SANDBOX
        t2 = TradingType.LIVE
        t3 = TradingType.BACKTEST
        assert t0 == TradingType.NONE
        assert t1 == TradingType.SANDBOX
        assert t2 == TradingType.LIVE
        assert t3 == TradingType.BACKTEST
        assert t0 == TradingType(0)
        assert t1 == TradingType(1)
        assert t2 == TradingType(2)
        assert t3 == TradingType(3)

    def test_exchange_type(self):
        from ..lib.enums import ExchangeType
        t0 = ExchangeType.NONE
        t1 = ExchangeType.BITSTAMP
        t2 = ExchangeType.BITFINEX
        t3 = ExchangeType.CEX
        t4 = ExchangeType.GDAX
        t5 = ExchangeType.GEMINI
        t6 = ExchangeType.HITBTC
        t7 = ExchangeType.ITBIT
        t8 = ExchangeType.KRAKEN
        t9 = ExchangeType.LAKE
        t10 = ExchangeType.POLONIEX
        assert t0 == ExchangeType.NONE
        assert t1 == ExchangeType.BITSTAMP
        assert t2 == ExchangeType.BITFINEX
        assert t3 == ExchangeType.CEX
        assert t4 == ExchangeType.GDAX
        assert t5 == ExchangeType.GEMINI
        assert t6 == ExchangeType.HITBTC
        assert t7 == ExchangeType.ITBIT
        assert t8 == ExchangeType.KRAKEN
        assert t9 == ExchangeType.LAKE
        assert t10 == ExchangeType.POLONIEX
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
        assert t10 == ExchangeType(10)

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
