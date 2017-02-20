import GDAX
import json
import os
import pprint
import websocket
# import thread
# import time
from ..callback import Callback
from ..config import ExchangeConfig
from ..enums import TradingType, ExchangeType, TickType, strToCurrencyType
from ..exchange import Exchange
from ...manual import manual
from ..structs import TradeRequest, TradeResponse, MarketData
from websocket import create_connection
from ..utils import trade_req_to_params_gdax, parse_date, get_keys_from_environment
from ..logging import LOG as log, TXN as tlog, OTHER as olog


class GDAXExchange(Exchange):
    def __init__(self, options: ExchangeConfig):
        super(GDAXExchange, self).__init__(options)
        self._type = ExchangeType.GDAX
        self._last = None

        if options.trading_type == TradingType.LIVE:
            self._key, self._secret, self._passphrase = get_keys_from_environment('GDAX')
            self._client = GDAX.AuthenticatedClient(self._key,
                                                    self._secret,
                                                    self._passphrase)

        elif options.trading_type == TradingType.SANDBOX:
            self._key, self._secret, self._passphrase = get_keys_from_environment('GDAX_SANDBOX')
            self._client = GDAX.AuthenticatedClient(self._key,
                                                    self._secret,
                                                    self._passphrase,
                                                    api_url="https://api-public.sandbox.gdax.com"
                                                    )

        self._ws_url = 'wss://ws-feed-public.sandbox.gdax.com'
        self._subscription = json.dumps({"type": "subscribe",
                                         "product_id": "BTC-USD"})
        self._heartbeat = json.dumps({"type": "heartbeat",
                                      "on": True})

        self._seqnum_enabled = True

    def run(self, engine):
        # DEBUG
        # websocket.enableTrace(True)

        while True:
            if not self._running:
                log.info('Starting....')
                self.ws = create_connection(self._ws_url)
                log.info('Connected!')

                self.ws.send(self._subscription)
                log.info('Sending Subscription %s' % self._subscription)
                self.ws.send(self._heartbeat)
                log.info('Sending Heartbeat %s' % self._subscription)

                self._running = True

            log.info('')
            log.info('Starting algo trading')
            try:
                while True:
                    self.receive()
                    engine.tick()

            except KeyboardInterrupt:
                x = manual(self)
                if x:
                    if x == 1:
                        log.warn('')
                        self._running = True
                    elif x == 2:
                        log.warn('')
                        log.warn('Halting algo trading')
                        self._running = False
                else:
                    log.info('')
                    log.critical('Terminating program')
                    self.close()
                    return
            # except Exception as e:
            #     log.critical(e)

            #     self.callback(TickType.ERROR, e)
            #     self.close()

            #     return

    def accountInfo(self):
        return pprint.pformat(self._client.getAccounts()) if hasattr(self, '_client') else 'BACKTEST'

    def sendOrder(self, callback: Callback):
        '''send order to exchange'''

    def orderResponse(self, response):
        '''parse the response'''

    def orderBook(self, level=1):
        '''get order book'''
        return self._client.getProductOrderBook(level=level)

    def buy(self, req: TradeRequest) -> TradeResponse:
        '''execute a buy order'''
        params = trade_req_to_params_gdax(req)
        log.warn(str(params))
        # self._client.buy(params)

    def sell(self, req: TradeRequest) -> TradeResponse:
        '''execute a sell order'''
        params = trade_req_to_params_gdax(req)
        log.warn(str(params))
        # self._client.sell(params)

    def tickToData(self, jsn):
        time = parse_date(jsn.get('time'))
        price = float(jsn.get('price', 'nan'))
        volume = float(jsn.get('size', 'nan'))
        typ = self.strToTradeType(jsn.get('type'))
        currency = strToCurrencyType(jsn.get('product_id'))

        remaining_volume = float(jsn.get('remaining_size', 'nan'))
        reason = jsn.get('reason', '')
        sequence = int(jsn.get('sequence'))

        ret = MarketData(time=time,
                         volume=volume,
                         price=price,
                         type=typ,
                         currency=currency,
                         remaining=remaining_volume,
                         reason=reason,
                         sequence=sequence)
        return ret

    @staticmethod
    def strToTradeType(s):
        if s == 'match':
            return TickType.MATCH
        elif s == 'received':
            return TickType.RECEIVED
        elif s == 'open':
            return TickType.OPEN
        elif s == 'done':
            return TickType.DONE
        elif s == 'change':
            return TickType.CHANGE
        elif s == 'heartbeat':
            return TickType.HEARTBEAT
        else:
            return TickType.ERROR
