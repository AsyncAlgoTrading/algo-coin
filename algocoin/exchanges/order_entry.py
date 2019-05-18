import ccxt
import pandas as pd
from functools import lru_cache
from ..data_source import RestAPIDataSource
from ..enums import PairType, TradingType, ExchangeType
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
        if options.trading_type == TradingType.SANDBOX:
            key, secret, passphrase = get_keys_from_environment(options.exchange_type.value + '_SANDBOX')
        else:
            key, secret, passphrase = get_keys_from_environment(options.exchange_type.value)

        return exchange_type_to_ccxt_client(options.exchange_type)({
            'apiKey': key,
            'secret': secret,
            'password': passphrase
            })

    def accounts(self):
        client = self.oe_client()
        if not client:
            return {}
        balances = client.fetch_balance()

        accounts = []

        for jsn in balances['info']:
            currency = str_to_currency_type(jsn['currency'])
            if 'balance' in jsn:
                balance = float(jsn['balance'])
            elif 'amount' in jsn:
                balance = float(jsn['amount'])

            id = jsn.get('id', jsn['currency'])

            account = Account(id=id, currency=currency, balance=balance)
            accounts.append(account)
        return accounts

    def currencyPairToStringCCXT(self, cur: PairType) -> str:
        return cur.value[0].value + '/' + cur.value[1].value

    def historical(self, timeframe='1m', since=None, limit=None):
        '''get historical data (for backtesting)'''
        client = self.oe_client()
        dfs = [{'pair': str(symbol), 'data': client.fetch_ohlcv(symbol=self.currencyPairToStringCCXT(symbol), timeframe=timeframe, since=since, limit=limit)}
               for symbol in self.options().currency_pairs]
        df = pd.io.json.json_normalize(dfs, 'data', ['pair'])
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'pair']
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index(['timestamp', 'pair'], inplace=True)
        df.sort_index(inplace=True)
        return df

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
