from mock import patch, MagicMock
from ...exchanges.helpers import CoinbaseHelpersMixin, GeminiHelpersMixin
from ...enums import TickType, CurrencyType, PairType


class TestExchangeHelpers:
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

    def test_CoinbaseHelpers_strToTradeType(self):
        assert CoinbaseHelpersMixin.strToTradeType('match') == TickType.TRADE
        assert CoinbaseHelpersMixin.strToTradeType('received') == TickType.RECEIVED
        assert CoinbaseHelpersMixin.strToTradeType('open') == TickType.OPEN
        assert CoinbaseHelpersMixin.strToTradeType('done') == TickType.DONE
        assert CoinbaseHelpersMixin.strToTradeType('change') == TickType.CHANGE
        assert CoinbaseHelpersMixin.strToTradeType('heartbeat') == TickType.HEARTBEAT
        assert CoinbaseHelpersMixin.strToTradeType('flarg') == TickType.ERROR

    def test_CoinbaseHelpers_currencyToString(self):
        assert CoinbaseHelpersMixin.currencyToString(CurrencyType.BTC) == 'BTC'
        assert CoinbaseHelpersMixin.currencyToString(CurrencyType.ETH) == 'ETH'
        assert CoinbaseHelpersMixin.currencyToString(CurrencyType.LTC) == 'LTC'
        assert CoinbaseHelpersMixin.currencyToString(CurrencyType.BCH) == 'BCH'

    def test_CoinbaseHelpers_currencyPairToString(self):
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.BTCUSD) == 'BTC-USD'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.BTCETH) == 'BTC-ETH'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.BTCLTC) == 'BTC-LTC'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.BTCBCH) == 'BTC-BCH'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.ETHUSD) == 'ETH-USD'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.LTCUSD) == 'LTC-USD'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.BCHUSD) == 'BCH-USD'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.ETHBTC) == 'ETH-BTC'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.LTCBTC) == 'LTC-BTC'
        assert CoinbaseHelpersMixin.currencyPairToString(PairType.BCHBTC) == 'BCH-BTC'

    def test_GeminiHelpers_reasonToTradeType(self):
        assert GeminiHelpersMixin.reasonToTradeType('CANCEL') == TickType.DONE
        assert GeminiHelpersMixin.reasonToTradeType('PLACE') == TickType.OPEN
        assert GeminiHelpersMixin.reasonToTradeType('INITIAL') == TickType.OPEN

    def test_GeminiHelpers_strToTradeType(self):
        assert GeminiHelpersMixin.strToTradeType('trade') == TickType.TRADE
        assert GeminiHelpersMixin.strToTradeType('change') == TickType.CHANGE
        assert GeminiHelpersMixin.strToTradeType('heartbeat') == TickType.HEARTBEAT
        assert GeminiHelpersMixin.strToTradeType('flarg') == TickType.ERROR

    def test_GeminiHelpers_currencyPairToString(self):
        assert GeminiHelpersMixin.currencyPairToString(PairType.BTCUSD) == 'BTCUSD'
        assert GeminiHelpersMixin.currencyPairToString(PairType.ETHUSD) == 'ETHUSD'
        assert GeminiHelpersMixin.currencyPairToString(PairType.ZECUSD) == 'ZECUSD'
        assert GeminiHelpersMixin.currencyPairToString(PairType.ETHBTC) == 'ETHBTC'
        assert GeminiHelpersMixin.currencyPairToString(PairType.ZECETH) == 'ZECETH'

    # def test_GeminiHelpers_currencyToString(self):
    #     assert GeminiHelpersMixin.currencyToString(CurrencyType.BTC) == 'BTC'
    #     assert GeminiHelpersMixin.currencyToString(CurrencyType.ETH) == 'ETH'
    #     assert GeminiHelpersMixin.currencyToString(CurrencyType.LTC) == 'LTC'
    #     assert GeminiHelpersMixin.currencyToString(CurrencyType.BCH) == 'BCH'
