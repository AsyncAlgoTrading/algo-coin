class TestDefine:
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

    def test_exchange_endpoint(self):
        from ..lib.define import EXCHANGE_MARKET_DATA_ENDPOINT
        from ..lib.enums import ExchangeType, TradingType

        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BITSTAMP, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BITSTAMP, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BITFINEX, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BITFINEX, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.CEX, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.CEX, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.GDAX, TradingType.SANDBOX) \
            == 'wss://ws-feed.sandbox.gdax.com'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.GDAX, TradingType.LIVE) \
            == 'wss://ws-feed.gdax.com'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.GEMINI, TradingType.SANDBOX) \
            == 'wss://api.sandbox.gemini.com/v1/marketdata/btcusd?heartbeat=true'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.GEMINI, TradingType.LIVE) \
            == 'wss://api.gemini.com/v1/marketdata/btcusd?heartbeat=true'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.HITBTC, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.HITBTC, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.ITBIT, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.ITBIT, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.KRAKEN, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.KRAKEN, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.LAKE, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.LAKE, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.POLONIEX, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.POLONIEX, TradingType.LIVE) \
            == ''
