import gdax
import json
from websocket import create_connection
from ..config import ExchangeConfig
from ..enums import TradingType, ExchangeType
from ..exchange import Exchange
from ..structs import TradeRequest, TradeResponse, Account
from ..utils import get_keys_from_environment, str_to_currency_type
from ..enums import CurrencyType, TradeResult
from ..logging import LOG as log
from .helpers import GDAXHelpersMixin


class GDAXExchange(GDAXHelpersMixin, Exchange):
    def __init__(self, options: ExchangeConfig) -> None:
        super(GDAXExchange, self).__init__(options)
        self._type = ExchangeType.GDAX
        self._last = None
        self._orders = {}

        if options.trading_type == TradingType.LIVE:
            self._key, self._secret, self._passphrase = get_keys_from_environment('GDAX')
            self._client = gdax.AuthenticatedClient(self._key,
                                                    self._secret,
                                                    self._passphrase)

        elif options.trading_type == TradingType.SANDBOX:
            self._key, self._secret, self._passphrase = get_keys_from_environment('GDAX_SANDBOX')
            self._client = gdax.AuthenticatedClient(self._key,
                                                    self._secret,
                                                    self._passphrase,
                                                    api_url=self._oe_url
                                                    )

        val = self._client.get_accounts() if hasattr(self, '_client') else []

        print(val)
        if isinstance(val, dict) and val.get('message') == 'Invalid API Key':
            raise Exception('Something went wrong with the API Key')

        self._accounts = []
        for jsn in val:
            currency = str_to_currency_type(jsn.get('currency'))
            balance = float(jsn.get('balance', 'inf'))
            id = jsn.get('id', 'id')
            account = Account(id=id, currency=currency, balance=balance)
            self._accounts.append(account)

        self._subscription = json.dumps({"type": "subscribe",
                                         "product_id": "BTC-USD"})
        self._heartbeat = json.dumps({"type": "heartbeat",
                                      "on": True})

        self._seqnum_enabled = True

    def run(self, engine) -> None:
        # DEBUG
        # websocket.enableTrace(True)

        while True:
            if not self._running and not self._manual:
                # startup and redundancy
                log.info('Starting....')
                self.ws = create_connection(self._md_url)
                log.info('Connected!')

                self.ws.send(self._subscription)
                log.info('Sending Subscription %s' % self._subscription)
                self.ws.send(self._heartbeat)
                log.info('Sending Heartbeat %s' % self._heartbeat)

                self._running = True

                log.info('')
                log.info('Starting algo trading')
            try:
                while True:
                    self.receive()
                    engine.tick()

            except KeyboardInterrupt:
                log.critical('Terminating program')
                return

    def accounts(self) -> list:
        return self._accounts

    def orderBook(self, level=1):
        '''get order book'''
        return self._client.getProductOrderBook(level=level)

    def buy(self, req: TradeRequest) -> TradeResponse:
        '''execute a buy order'''
        params = GDAXExchange.trade_req_to_params(req)
        log.warn("Buy params: %s", str(params))
        res = self._client.buy(**params)
        return TradeResponse(request=req,
                             side=req.side,
                             volume=0.0,
                             price=0.0,
                             currency=CurrencyType.BTC,
                             slippage=0.0,
                             transaction_cost=0.0,
                             status=TradeResult.FILLED)

    def sell(self, req: TradeRequest) -> TradeResponse:
        '''execute a sell order'''
        params = GDAXExchange.trade_req_to_params(req)
        log.warn("Sell params: %s", str(params))
        res = self._client.sell(**params)
        return TradeResponse(request=req,
                             side=req.side,
                             volume=0.0,
                             price=0.0,
                             currency=CurrencyType.BTC,
                             slippage=0.0,
                             transaction_cost=0.0,
                             status=TradeResult.FILLED)
