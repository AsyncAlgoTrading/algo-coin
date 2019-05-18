import ccxt
from functools import lru_cache
from ..data_source import RestAPIDataSource
from ..enums import TradingType, ExchangeType
from ..structs import TradeRequest, TradeResponse, Account
from ..utils import get_keys_from_environment, str_to_currency_type
# from ..logging import LOG as log


def exchange_type_to_ccxt_client(exchange_type):
    if exchange_type == ExchangeType.COINBASE:
        return ccxt.coinbasepro
    elif exchange_type == ExchangeType.GEMINI:
        return ccxt.gemini
    elif exchange_type == ExchangeType.POLONIEX:
        return ccxt.poloniex


class CCXTOrderEntryMixin(RestAPIDataSource):
    @lru_cache(None)
    def oe_client(self):
        options = self.options()
        if options.trading_type == TradingType.LIVE or options.trading_type == TradingType.SIMULATION:
            key, secret, passphrase = get_keys_from_environment(options.ccxt_exchange.value)
        elif options.trading_type == TradingType.SANDBOX:
            key, secret, passphrase = get_keys_from_environment(options.ccxt_exchange.value + '_SANDBOX')

        if options.trading_type in (TradingType.LIVE, TradingType.SIMULATION, TradingType.SANDBOX):
            try:
                client = exchange_type_to_ccxt_client(options.ccxt_exchange)({
                    'apiKey': key,
                    'secret': secret,
                    'password': passphrase
                    })
            except Exception:
                raise Exception('Something went wrong with the API Key/Client instantiation')
            return client

    def accounts(self):
        client = self.oe_client()
        if not client:
            return {}
        balances = client.fetch_balance()

        accounts = []

        for jsn in balances['info']:
            currency = str_to_currency_type(jsn.get('currency'))
            balance = float(jsn.get('balance', 'inf'))
            id = jsn.get('id', 'id')
            account = Account(id=id, currency=currency, balance=balance)
            accounts.append(account)
        return accounts

    def orderBook(self, level=1):
        '''get order book'''
        return self.oe_client().getProductOrderBook(level=level)

    def buy(self, req: TradeRequest) -> TradeResponse:
        '''execute a buy order'''

    def sell(self, req: TradeRequest) -> TradeResponse:
        '''execute a sell order'''

    def cancel(self, resp: TradeResponse):
        raise NotImplementedError()

    def cancelAll(self, resp: TradeResponse):
        raise NotImplementedError()
