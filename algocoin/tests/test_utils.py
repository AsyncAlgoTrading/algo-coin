class TestUtils:
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

    def test_config(self):
        from ..lib.utils import config

        @config
        class Test:
            a = int
            b = str, ''
            c = [str]
            d = [str], ['']

        t = Test()
        t.a = 5

        assert t.a == 5
        assert t.b == ''

        try:
            t.a = ''
            assert False
        except:
            pass

        t.b = 'test'
        assert t.b == 'test'

        t.c = ['test']
        assert t.c == ['test']
        assert t.d == ['']

    def test_struct(self):
        from ..lib.utils import struct

        @struct
        class Test:
            a = int
            b = str

        t = Test(a=5, b='')

        assert t.a == 5
        assert t.b == ''

    def test_parse_date(self):
        from datetime import datetime
        from ..lib.utils import parse_date
        gold = datetime(2016, 11, 16, 0, 0)
        date1 = parse_date('1479272400.0')
        date2 = parse_date('2016-11-16T00:00:00.000000Z')
        print(gold)
        print(date1)
        print(date2)

        assert gold == date1 == date2

    def test_struct_warnings(self):
        from ..lib.utils import struct

        @struct
        class Test:
            a = int, 5

        t = Test()

        try:
            print(t.a)
            assert False
        except:
            pass
        t.a = 5
        assert t.a == 5

    def test_ex_type_to_ex(self):
        from ..lib.utils import ex_type_to_ex
        from ..lib.enums import ExchangeType
        from ..lib.exchanges.gdax import GDAXExchange
        assert ex_type_to_ex(ExchangeType.GDAX) == GDAXExchange

    def test_exchange_to_file(self):
        from ..lib.utils import exchange_to_file
        from ..lib.enums import ExchangeType

        assert(exchange_to_file(ExchangeType.GDAX),
               "./data/exchange/coinbaseUSD.csv")
        assert(exchange_to_file(ExchangeType.BITSTAMP),
               "./data/exchange/bitstampUSD.csv")
        assert(exchange_to_file(ExchangeType.BITFINEX),
               "./data/exchange/bitfinexUSD.csv")
        assert(exchange_to_file(ExchangeType.ITBIT),
               "./data/exchange/itbitUSD.csv")
        assert(exchange_to_file(ExchangeType.KRAKEN),
               "./data/exchange/krakenUSD.csv")
        assert(exchange_to_file(ExchangeType.HITBTC),
               "./data/exchange/hitbtcUSD.csv")
        assert(exchange_to_file(ExchangeType.LAKE),
               "./data/exchange/lakeUSD.csv")

    def test_set_verbose(self):
        import logging
        from ..lib.utils import set_verbose
        from ..lib.logging import LOG as log, \
            STRAT as slog, \
            DATA as dlog, \
            RISK as rlog, \
            EXEC as exlog, \
            SLIP as sllog, \
            TXNS as tlog, \
            MANUAL as mlog, \
            ERROR as elog
        set_verbose(2)

        assert(log.level == logging.DEBUG)
        assert(slog.level == logging.DEBUG)
        assert(dlog.level == logging.DEBUG)
        assert(rlog.level == logging.DEBUG)
        assert(exlog.level == logging.DEBUG)
        assert(sllog.level == logging.DEBUG)
        assert(tlog.level == logging.DEBUG)
        assert(mlog.level == logging.DEBUG)
        assert(elog.level == logging.DEBUG)

    def test_get_keys_from_environment(self):
        from ..lib.utils import get_keys_from_environment
        import os
        os.environ['TEST_API_KEY'] = 'test'
        os.environ['TEST_API_SECRET'] = 'test'
        os.environ['TEST_API_PASS'] = 'test'
        one, two, three = get_keys_from_environment('TEST')
        assert(one == 'test')
        assert(two == 'test')
        assert(three == 'test')

    def test_str_to_currency_type(self):
        from ..lib.utils import str_to_currency_type
        from ..lib.enums import CurrencyType
        assert(str_to_currency_type('BTC') == CurrencyType.BTC)
        assert(str_to_currency_type('ETH') == CurrencyType.ETH)
        assert(str_to_currency_type('LTC') == CurrencyType.LTC)
        assert(str_to_currency_type('USD') == CurrencyType.USD)

    def test_str_to_side(self):
        from ..lib.utils import str_to_side
        from ..lib.enums import Side
        assert(str_to_side('BUY') == Side.BUY)
        assert(str_to_side('SELL') == Side.SELL)
        assert(str_to_side('OTHER') == Side.NONE)

    def test_str_to_order_type(self):
        from ..lib.utils import str_to_order_type
        from ..lib.enums import OrderType
        assert(str_to_order_type('MARKET') == OrderType.MARKET)
        assert(str_to_order_type('LIMIT') == OrderType.LIMIT)
        assert(str_to_order_type('OTHER') == OrderType.NONE)

    def test_str_to_exchange(self):
        from ..lib.utils import str_to_exchange
        from ..lib.enums import ExchangeType
        assert(str_to_exchange('bitfinex') == ExchangeType.BITFINEX)
        assert(str_to_exchange('bitstamp') == ExchangeType.BITSTAMP)
        assert(str_to_exchange('gemini') == ExchangeType.GEMINI)
        assert(str_to_exchange('hitbtc') == ExchangeType.HITBTC)
        assert(str_to_exchange('itbit') == ExchangeType.ITBIT)
        assert(str_to_exchange('kraken') == ExchangeType.KRAKEN)
        assert(str_to_exchange('lake') == ExchangeType.LAKE)
        assert(str_to_exchange('gdax') == ExchangeType.GDAX)
