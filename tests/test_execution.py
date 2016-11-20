class TestExecution:
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

    def test_init(self):
        from execution import Execution
        from exchange import Exchange
        from config import ExecutionConfig, ExchangeConfig

        exc = ExchangeConfig()
        ex = Exchange(exc)

        ec = ExecutionConfig()
        e = Execution(ec, ex)
        assert e

    def test_request(self):
        from execution import Execution
        from exchange import Exchange
        from enums import Side, ExchangeType, CurrencyType, \
            OrderType, OrderSubType
        from config import ExecutionConfig, ExchangeConfig
        from structs import TradeRequest

        exc = ExchangeConfig()
        ex = Exchange(exc)

        ec = ExecutionConfig()
        e = Execution(ec, ex)

        req = TradeRequest(side=Side.BUY,
                           volume=1.0,
                           price=1.0,
                           exchange=ExchangeType.GDAX,
                           currency=CurrencyType.BTC,
                           order_type=OrderType.LIMIT,
                           order_sub_type=OrderSubType.NONE)

        resp = e.request(req)
