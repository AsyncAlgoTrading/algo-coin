from types import ExchangeType, TradingType


EXCHANGE_ENDPOINT = lambda name, typ: {
    (ExchangeType.BITSTAMP, TradingType.PAPER): '',
    (ExchangeType.BITSTAMP, TradingType.REAL): '',
    (ExchangeType.BITFINEX, TradingType.PAPER): '',
    (ExchangeType.BITFINEX, TradingType.REAL): 'wss://api2.bitfinex.com:3000/ws',
    (ExchangeType.BTCC, TradingType.PAPER): '',
    (ExchangeType.BTCC, TradingType.REAL): '',
    (ExchangeType.CEX, TradingType.PAPER): '',
    (ExchangeType.CEX, TradingType.REAL): 'wss://ws.cex.io/ws/',
    (ExchangeType.GDAX, TradingType.PAPER): 'wss://ws-feed-public.sandbox.gdax.com',
    (ExchangeType.GDAX, TradingType.REAL): 'wss://ws-feed.exchange.coinbase.com',
    (ExchangeType.GEMINI, TradingType.PAPER): '',
    (ExchangeType.GEMINI, TradingType.REAL): 'wss://api.gemini.com/v1/marketdata/:symbol',
    (ExchangeType.HITBTC, TradingType.PAPER): 'wss://demo-api.hitbtc.com:8080',
    (ExchangeType.HITBTC, TradingType.REAL): 'wss://api.hitbtc.com:8080',
    (ExchangeType.POLONIEX, TradingType.PAPER): '',
    (ExchangeType.POLONIEX, TradingType.REAL): 'wss://api.poloniex.com',
}.get((name, typ))
