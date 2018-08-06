import os
from mock import patch, MagicMock


class TestOrderEntry:
    def setup(self):
        # setup() before each test method
        from algocoin.lib.config import ExchangeConfig
        from algocoin.lib.enums import TradingType, ExchangeType, PairType

        os.environ['GEMINI_API_KEY'] = 'test'
        os.environ['GEMINI_API_SECRET'] = 'test'
        os.environ['GEMINI_API_PASS'] = 'test'

        self.ec = ExchangeConfig(exchange_type=ExchangeType.GEMINI, trading_type=TradingType.LIVE, currency_pairs=[PairType.BTCUSD])

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

    def test_OE(self):
        from algocoin.lib.oe import OrderEntry
        with patch('ccxt.__getattribute__') as m:
            oe = OrderEntry(self.ec, MagicMock())
            print(oe)
            assert m.call_count == 1
