from functools import lru_cache
from .enums import ExchangeType, TradingType


EXCHANGE_MARKET_DATA_ENDPOINT = lru_cache(None)(lambda name, typ: {  # noqa: E731
    (ExchangeType.BITSTAMP, TradingType.SANDBOX): '',
    (ExchangeType.BITSTAMP, TradingType.SIMULATION): '',
    (ExchangeType.BITSTAMP, TradingType.LIVE): '',

    (ExchangeType.BITFINEX, TradingType.SANDBOX): '',
    (ExchangeType.BITFINEX, TradingType.LIVE): '',

    (ExchangeType.CEX, TradingType.SANDBOX): '',
    (ExchangeType.CEX, TradingType.LIVE): '',

    (ExchangeType.COINBASE, TradingType.SANDBOX): 'wss://ws-feed.sandbox.gdax.com',
    (ExchangeType.COINBASE, TradingType.LIVE): 'wss://ws-feed-public.sandbox.pro.coinbase.com',
    (ExchangeType.COINBASE, TradingType.SIMULATION): 'wss://ws-feed-public.sandbox.pro.coinbase.com',


    (ExchangeType.COINBASE, TradingType.SANDBOX): 'wss://ws-feed.pro.pro.coinbase.com',
    (ExchangeType.COINBASE, TradingType.LIVE): 'wss://ws-feed.pro.coinbase.com',
    (ExchangeType.COINBASE, TradingType.SIMULATION): 'wss://ws-feed.pro.coinbase.com',

    (ExchangeType.GEMINI, TradingType.SANDBOX): 'wss://api.sandbox.gemini.com/v1/marketdata/%s?heartbeat=true',
    (ExchangeType.GEMINI, TradingType.LIVE): 'wss://api.gemini.com/v1/marketdata/%s?heartbeat=true',
    (ExchangeType.GEMINI, TradingType.SIMULATION): 'wss://api.gemini.com/v1/marketdata/%s?heartbeat=true',

    (ExchangeType.HITBTC, TradingType.SANDBOX): '',
    (ExchangeType.HITBTC, TradingType.LIVE): '',
    (ExchangeType.HITBTC, TradingType.SIMULATION): '',

    (ExchangeType.ITBIT, TradingType.SANDBOX): '',
    (ExchangeType.ITBIT, TradingType.LIVE): '',
    (ExchangeType.ITBIT, TradingType.SIMULATION): '',

    (ExchangeType.KRAKEN, TradingType.SANDBOX): '',
    (ExchangeType.KRAKEN, TradingType.LIVE): '',
    (ExchangeType.KRAKEN, TradingType.SIMULATION): '',

    (ExchangeType.LAKE, TradingType.SANDBOX): '',
    (ExchangeType.LAKE, TradingType.LIVE): '',
    (ExchangeType.LAKE, TradingType.SIMULATION): '',

    (ExchangeType.POLONIEX, TradingType.SANDBOX): '',
    (ExchangeType.POLONIEX, TradingType.LIVE): '',
    (ExchangeType.POLONIEX, TradingType.SIMULATION): '',

    (ExchangeType.DERIBIT, TradingType.SANDBOX): 'wss://test.deribit.com/ws/api/v1/',
    (ExchangeType.DERIBIT, TradingType.LIVE): 'wss://www.deribit.com/ws/api/v1/',
    (ExchangeType.DERIBIT, TradingType.SIMULATION): 'wss://www.deribit.com/ws/api/v1/',

}.get((name, typ), None))

EXCHANGE_ORDER_ENDPOINT = lru_cache(None)(lambda name, typ: {  # noqa: E731
    (ExchangeType.BITSTAMP, TradingType.SANDBOX): '',
    (ExchangeType.BITSTAMP, TradingType.LIVE): '',

    (ExchangeType.BITFINEX, TradingType.SANDBOX): '',
    (ExchangeType.BITFINEX, TradingType.LIVE): '',

    (ExchangeType.CEX, TradingType.SANDBOX): '',
    (ExchangeType.CEX, TradingType.LIVE): '',

    (ExchangeType.GDAX, TradingType.SANDBOX): 'https://api-public.sandbox.gdax.com',
    (ExchangeType.GDAX, TradingType.LIVE): 'https://api.gdax.com',
    (ExchangeType.GDAX, TradingType.SIMULATION): 'https://api.gdax.com',

    (ExchangeType.COINBASE, TradingType.SANDBOX): 'https://api-public.sandbox.pro.coinbase.com',
    (ExchangeType.COINBASE, TradingType.LIVE): 'https://api.pro.coinbase.com',
    (ExchangeType.COINBASE, TradingType.SIMULATION): 'https://api.pro.coinbase.com',

    (ExchangeType.GEMINI, TradingType.SANDBOX): 'https://api.sandbox.gemini.com/v1/marketdata/btcusd?heartbeat=true',
    (ExchangeType.GEMINI, TradingType.LIVE): 'https://api.gemini.com/v1/marketdata/btcusd?heartbeat=true',
    (ExchangeType.GEMINI, TradingType.SIMULATION): 'https://api.gemini.com/v1/marketdata/btcusd?heartbeat=true',

    (ExchangeType.HITBTC, TradingType.SANDBOX): '',
    (ExchangeType.HITBTC, TradingType.LIVE): '',

    (ExchangeType.ITBIT, TradingType.SANDBOX): '',
    (ExchangeType.ITBIT, TradingType.LIVE): '',

    (ExchangeType.KRAKEN, TradingType.SANDBOX): '',
    (ExchangeType.KRAKEN, TradingType.LIVE): '',

    (ExchangeType.LAKE, TradingType.SANDBOX): '',
    (ExchangeType.LAKE, TradingType.LIVE): '',

    (ExchangeType.POLONIEX, TradingType.SANDBOX): '',
    (ExchangeType.POLONIEX, TradingType.LIVE): '',

    (ExchangeType.DERIBIT, TradingType.SANDBOX): 'https://test.deribit.com',
    (ExchangeType.DERIBIT, TradingType.LIVE): 'https://www.deribit.com',
    (ExchangeType.DERIBIT, TradingType.SIMULATION): 'https://www.deribit.com',

}.get((name, typ), None))

ACCOUNTS = lambda name, typ: {  # noqa: E731
    (ExchangeType.BITSTAMP, TradingType.SANDBOX): '',
    (ExchangeType.BITSTAMP, TradingType.LIVE): '',

    (ExchangeType.BITFINEX, TradingType.SANDBOX): '',
    (ExchangeType.BITFINEX, TradingType.LIVE): '',

    (ExchangeType.CEX, TradingType.SANDBOX): '',
    (ExchangeType.CEX, TradingType.LIVE): '',

    (ExchangeType.GDAX, TradingType.SANDBOX): 'https://api-public.sandbox.gdax.com',
    (ExchangeType.GDAX, TradingType.LIVE): 'https://api.gdax.com',
    (ExchangeType.GDAX, TradingType.SIMULATION): 'https://api.gdax.com',

    (ExchangeType.GEMINI, TradingType.SANDBOX): 'https://api.sandbox.gemini.com',
    (ExchangeType.GEMINI, TradingType.LIVE): 'https://api.gemini.com',
    (ExchangeType.GEMINI, TradingType.SIMULATION): 'https://api.gemini.com',

    (ExchangeType.HITBTC, TradingType.SANDBOX): '',
    (ExchangeType.HITBTC, TradingType.LIVE): '',

    (ExchangeType.ITBIT, TradingType.SANDBOX): '',
    (ExchangeType.ITBIT, TradingType.LIVE): '',

    (ExchangeType.KRAKEN, TradingType.SANDBOX): '',
    (ExchangeType.KRAKEN, TradingType.LIVE): '',

    (ExchangeType.LAKE, TradingType.SANDBOX): '',
    (ExchangeType.LAKE, TradingType.LIVE): '',

    (ExchangeType.POLONIEX, TradingType.SANDBOX): '',
    (ExchangeType.POLONIEX, TradingType.LIVE): '',

    (ExchangeType.DERIBIT, TradingType.SANDBOX): 'https://test.deribit.com',
    (ExchangeType.DERIBIT, TradingType.LIVE): 'https://www.deribit.com',
    (ExchangeType.DERIBIT, TradingType.SIMULATION): 'https://www.deribit.com',

}.get((name, typ), None)
