// tslint:disable: object-literal-sort-keys
export const APIS = {
    ACCOUNTS: "/api/v1/json/accounts",
    EXCHANGES: "/api/v1/json/exchanges",
    INSTRUMENTS: "/api/v1/json/instruments",
    LAST_PRICE: "/api/v1/arrow/last-price-all",
    MYORDERS: "/api/v1/arrow/myorders",
    MYTRADES: "/api/v1/arrow/mytrades",
    STRATEGIES: "/api/v1/arrow/strategies",
    STRATEGY_TRADE_REQUESTS: "/api/v1/arrow/strategy-trade-requests",
    STRATEGY_TRADE_RESPONSES: "/api/v1/arrow/strategy-trade-responses",
    TRADES: "/api/v1/arrow/trades",
};

export const COMMANDS = {
    HISTORICALDATA_OHLCV: "marketData:historicalDta:ohlcv",
    LIVEDATA_ORDERBOOK: "marketData:liveData:orderbook",
    LIVEDATA_LAST_PRICE: "marketData:liveData:lastPrice",
    LIVEDATA_TRADES: "marketData:liveData:trades",
    LIVEDATA_TRADES_BY_EXCH_ASSET: "marketData:liveData:tradesByExchangeAndAsset",
};
export const COMMAND_ICONS = {
    LIVEDATA_TRADES: "fa fa-plus",
};

export const INTERVAL = {
    ONE_SECOND: 1000,
    FIVE_SECONDS: 1000 * 5,
    TEN_SECONDS: 1000 * 10,
    ONE_MINUTE: 1000 * 60,
    FIVE_MINUTES: 1000 * 60 * 5,
    TEN_MINUTES: 1000 * 60 * 5,
};
