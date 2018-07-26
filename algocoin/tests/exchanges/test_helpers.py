from mock import patch, MagicMock
from ...lib.exchanges.helpers import GDAXHelpersMixin, GeminiHelpersMixin
from ...lib.enums import TickType, CurrencyType, PairType


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

    def test_GDAXHelpers_strToTradeType(self):
        assert GDAXHelpersMixin.strToTradeType('match') == TickType.TRADE
        assert GDAXHelpersMixin.strToTradeType('received') == TickType.RECEIVED
        assert GDAXHelpersMixin.strToTradeType('open') == TickType.OPEN
        assert GDAXHelpersMixin.strToTradeType('done') == TickType.DONE
        assert GDAXHelpersMixin.strToTradeType('change') == TickType.CHANGE
        assert GDAXHelpersMixin.strToTradeType('heartbeat') == TickType.HEARTBEAT
        assert GDAXHelpersMixin.strToTradeType('flarg') == TickType.ERROR

    def test_GDAXHelpers_currencyToString(self):
        assert GDAXHelpersMixin.currencyToString(CurrencyType.BTC) == 'BTC'
        assert GDAXHelpersMixin.currencyToString(CurrencyType.ETH) == 'ETH'
        assert GDAXHelpersMixin.currencyToString(CurrencyType.LTC) == 'LTC'
        assert GDAXHelpersMixin.currencyToString(CurrencyType.BCH) == 'BCH'

    def test_GDAXHelpers_currencyPairToString(self):
        assert GDAXHelpersMixin.currencyPairToString(PairType.BTCUSD) == 'BTC-USD'
        assert GDAXHelpersMixin.currencyPairToString(PairType.BTCETH) == 'BTC-ETH'
        assert GDAXHelpersMixin.currencyPairToString(PairType.BTCLTC) == 'BTC-LTC'
        assert GDAXHelpersMixin.currencyPairToString(PairType.BTCBCH) == 'BTC-BCH'
        assert GDAXHelpersMixin.currencyPairToString(PairType.ETHUSD) == 'ETH-USD'
        assert GDAXHelpersMixin.currencyPairToString(PairType.LTCUSD) == 'LTC-USD'
        assert GDAXHelpersMixin.currencyPairToString(PairType.BCHUSD) == 'BCH-USD'
        assert GDAXHelpersMixin.currencyPairToString(PairType.ETHBTC) == 'ETH-BTC'
        assert GDAXHelpersMixin.currencyPairToString(PairType.LTCBTC) == 'LTC-BTC'
        assert GDAXHelpersMixin.currencyPairToString(PairType.BCHBTC) == 'BCH-BTC'

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
