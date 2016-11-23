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
        from define import EXCHANGE_MARKET_DATA_ENDPOINT
        from enums import ExchangeType, TradingType

        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BITSTAMP, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BITSTAMP, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BITFINEX, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BITFINEX, TradingType.LIVE) \
            == 'wss://api2.bitfinex.com:3000/ws'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BTCC, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.BTCC, TradingType.LIVE) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.CEX, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.CEX, TradingType.LIVE) \
            == 'wss://ws.cex.io/ws/'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.GDAX, TradingType.SANDBOX) \
            == 'wss://ws-feed-public.sandbox.gdax.com'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.GDAX, TradingType.LIVE) \
            == 'wss://ws-feed.exchange.coinbase.com'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.GEMINI, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.GEMINI, TradingType.LIVE) \
            == 'wss://api.gemini.com/v1/marketdata/:symbol'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.HITBTC, TradingType.SANDBOX) \
            == 'wss://demo-api.hitbtc.com:8080'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.HITBTC, TradingType.LIVE) \
            == 'wss://api.hitbtc.com:8080'
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.POLONIEX, TradingType.SANDBOX) \
            == ''
        assert EXCHANGE_MARKET_DATA_ENDPOINT(ExchangeType.POLONIEX, TradingType.LIVE) \
            == 'wss://api.poloniex.com'
