import GDAX
import json
import os
import pprint
import websocket
import threading
import queue
# import time
from ..callback import Callback
from ..config import ExchangeConfig
from ..enums import TradingType, ExchangeType, TickType, strToCurrencyType
from ..exchange import Exchange
from ...manual import manual
from ..structs import TradeRequest, TradeResponse, MarketData, Account
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
                                                    api_url=self._oe_url
                                                    )

        self._accounts = []
        val = self._client.getAccounts() if hasattr(self, '_client') else ['BACKTEST']
        for jsn in val:
            currency = strToCurrencyType(jsn.get('currency'))
            balance = float(jsn.get('balance', 'inf'))
            id = jsn.get('id', 'id')
            account = Account(id=id, currency=currency, balance=balance)
            self._accounts.append(account)

        self._subscription = json.dumps({"type": "subscribe",
                                         "product_id": "BTC-USD"})
        self._heartbeat = json.dumps({"type": "heartbeat",
                                      "on": True})

        self._seqnum_enabled = True

    def run(self, engine):
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
                log.info('Sending Heartbeat %s' % self._subscription)

                self._running = True

                t, inqueue, outqueue = None, None, None

                log.info('')
                log.info('Starting algo trading')
            try:
                while True:
                    self.receive()
                    engine.tick()
                    if self._manual and t and t.is_alive():
                        try:
                            x = outqueue.get(block=False)
                            if x:
                                if x[0] == 'c':
                                    if not self._running:
                                        log.warn('Continuing algo trading')

                                    self._running = True
                                    engine.continueTrading()

                                elif x[0] == 'h':
                                    if self._running:
                                        log.warn('Halting algo trading')

                                    self._running = False
                                    engine.haltTrading()

                                elif x[0] == 'q':
                                    log.critical('Terminating program')

                                    self.close()
                                    inqueue.put(1)

                                    self._manual = False

                                    t.join()
                                    t = None
                                    return

                                elif x[0] == 'r':
                                    log.critical('leaving manual')

                                    inqueue.put(1)

                                    self._manual = False

                                    t.join()
                                    t = None
                                elif x[0] == 'b':
                                    self.buy(x[1])
                                elif x[0] == 's':
                                    self.sell(x[1])
                                else:
                                    log.critical('manual override error')
                        except queue.Empty:
                            pass

                    elif self._manual and t:
                        log.critical('leaving manual')
                        self._manual = False

                        t.join()
                        t = None

            except KeyboardInterrupt:
                # x = manual(self)
                if not self._manual:
                    self._manual = True
                    inqueue = queue.Queue()
                    outqueue = queue.Queue()
                    t = threading.Thread(target=manual, args=(self, inqueue, outqueue,))
                    t.start()
                else:
                    log.critical('Terminating program')
                    inqueue.put(1)
                    t.join()
                    return

            # except Exception as e:
            #     log.critical(e)

            #     self.callback(TickType.ERROR, e)
            #     self.close()

            #     return

    def accounts(self):
        # return pprint.pformat(self._client.getAccounts()) if hasattr(self, '_client') else 'BACKTEST'
        return self._accounts

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
