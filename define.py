from enums import ExchangeType, TradingType


EXCHANGE_MARKET_DATA_ENDPOINT = lambda name, typ: {
    (ExchangeType.BITSTAMP, TradingType.SANDBOX): '',
    (ExchangeType.BITSTAMP, TradingType.LIVE): '',
    (ExchangeType.BITFINEX, TradingType.SANDBOX): '',
    (ExchangeType.BITFINEX, TradingType.LIVE): 'wss://api2.bitfinex.com:3000/ws',
    (ExchangeType.BTCC, TradingType.SANDBOX): '',
    (ExchangeType.BTCC, TradingType.LIVE): '',
    (ExchangeType.CEX, TradingType.SANDBOX): '',
    (ExchangeType.CEX, TradingType.LIVE): 'wss://ws.cex.io/ws/',
    (ExchangeType.GDAX, TradingType.SANDBOX): 'wss://ws-feed-public.sandbox.gdax.com',
    (ExchangeType.GDAX, TradingType.LIVE): 'wss://ws-feed.exchange.coinbase.com',
    (ExchangeType.GEMINI, TradingType.SANDBOX): '',
    (ExchangeType.GEMINI, TradingType.LIVE): 'wss://api.gemini.com/v1/marketdata/:symbol',
    (ExchangeType.HITBTC, TradingType.SANDBOX): 'wss://demo-api.hitbtc.com:8080',
    (ExchangeType.HITBTC, TradingType.LIVE): 'wss://api.hitbtc.com:8080',
    (ExchangeType.POLONIEX, TradingType.SANDBOX): '',
    (ExchangeType.POLONIEX, TradingType.LIVE): 'wss://api.poloniex.com',
}.get((name, typ), None)

EXCHANGE_ORDER_ENDPOINT = lambda name, typ: {
    (ExchangeType.BITSTAMP, TradingType.SANDBOX): '',
    (ExchangeType.BITSTAMP, TradingType.LIVE): '',
    (ExchangeType.BITFINEX, TradingType.SANDBOX): '',
    (ExchangeType.BITFINEX, TradingType.LIVE): '',
    (ExchangeType.BTCC, TradingType.SANDBOX): '',
    (ExchangeType.BTCC, TradingType.LIVE): '',
    (ExchangeType.CEX, TradingType.SANDBOX): '',
    (ExchangeType.CEX, TradingType.LIVE): '',
    (ExchangeType.GDAX, TradingType.SANDBOX): 'https://api-public.sandbox.gdax.com',
    (ExchangeType.GDAX, TradingType.LIVE): 'https://api.gdax.com',
    (ExchangeType.GEMINI, TradingType.SANDBOX): '',
    (ExchangeType.GEMINI, TradingType.LIVE): '',
    (ExchangeType.HITBTC, TradingType.SANDBOX): '',
    (ExchangeType.HITBTC, TradingType.LIVE): '',
    (ExchangeType.POLONIEX, TradingType.SANDBOX): '',
    (ExchangeType.POLONIEX, TradingType.LIVE): '',
}.get((name, typ), None)

ACCOUNTS = lambda name, typ: {
    (ExchangeType.BITSTAMP, TradingType.SANDBOX): '',
    (ExchangeType.BITSTAMP, TradingType.LIVE): '',
    (ExchangeType.BITFINEX, TradingType.SANDBOX): '',
    (ExchangeType.BITFINEX, TradingType.LIVE): '',
    (ExchangeType.BTCC, TradingType.SANDBOX): '',
    (ExchangeType.BTCC, TradingType.LIVE): '',
    (ExchangeType.CEX, TradingType.SANDBOX): '',
    (ExchangeType.CEX, TradingType.LIVE): '',
    (ExchangeType.GDAX, TradingType.SANDBOX): 'https://api-public.sandbox.gdax.com',
    (ExchangeType.GDAX, TradingType.LIVE): 'https://api.gdax.com',
    (ExchangeType.GEMINI, TradingType.SANDBOX): '',
    (ExchangeType.GEMINI, TradingType.LIVE): '',
    (ExchangeType.HITBTC, TradingType.SANDBOX): '',
    (ExchangeType.HITBTC, TradingType.LIVE): '',
    (ExchangeType.POLONIEX, TradingType.SANDBOX): '',
    (ExchangeType.POLONIEX, TradingType.LIVE): '',
}.get((name, typ), None)

