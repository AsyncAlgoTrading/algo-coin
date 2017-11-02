from mock import patch
from datetime import datetime


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
        from ..execution import Execution
        from ..lib.exchanges.gdax import GDAXExchange
        from ..lib.config import ExecutionConfig, ExchangeConfig
        from ..lib.enums import ExchangeType

        with patch('os.environ'), patch('gdax.AuthenticatedClient'):
            exc = ExchangeConfig()
            exc.exchange_type = ExchangeType.GDAX
            ex = GDAXExchange(exc)

            ec = ExecutionConfig()
            e = Execution(ec, ex)
            assert e

    def test_request(self):
        from ..execution import Execution
        from ..lib.exchanges.gdax import GDAXExchange
        from ..lib.enums import Side, ExchangeType, TradingType
        from ..lib.config import ExecutionConfig, ExchangeConfig
        from ..lib.structs import TradeRequest

        with patch('os.environ'), patch('gdax.AuthenticatedClient'):
            exc = ExchangeConfig()
            exc.exchange_type = ExchangeType.GDAX
            exc.trading_type = TradingType.LIVE
            ex = GDAXExchange(exc)

            ec = ExecutionConfig()
            e = Execution(ec, ex)

            req = TradeRequest(side=Side.BUY,
                               volume=1.0,
                               price=1.0)

            resp = e.request(req)
