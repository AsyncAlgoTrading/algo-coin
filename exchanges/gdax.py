import GDAX
import json
import os
from callback import Callback
from config import ExchangeConfig
from enums import TradingType
from exchange import Exchange
from structs import TradeRequest, TradeResponse, ExecutionReport
from websocket import create_connection


class GDAXExchange(Exchange):
    def __init__(self, options: ExchangeConfig):
        super(GDAXExchange, self).__init__(options)
        self._lastseqnum = -1
        self._missingseqnum = set()

        if options.trading_type == TradingType.LIVE:
            self._key = os.environ['GDAX_API_KEY']
            self._secret = os.environ['GDAX_API_SECRET']
            self._passphrase = os.environ['GDAX_API_PASS']
            self.client = GDAX.AuthenticatedClient(self._key,
                                                   self._secret,
                                                   self._passphrase)

        else:
            self._key = os.environ['GDAX_SANDBOX_API_KEY']
            self._secret = os.environ['GDAX_SANDBOX_API_SECRET']
            self._passphrase = os.environ['GDAX_SANDBOX_API_PASS']
            self.client = GDAX.AuthenticatedClient(self._key,
                                                   self._secret,
                                                   self._passphrase,
                                                   api_url="https://api-public.sandbox.gdax.com"
                                                   )

    def run(self, engine):
        print('Starting....')
        self.ws = create_connection('wss://ws-feed.exchange.coinbase.com')
        print('Connected!')

        sub = json.dumps({"type": "subscribe",
                          "product_id": "BTC-USD"})
        self.ws.send(sub)
        print('Sending Subscription %s' % sub)

        try:
            while True:
                self._receive()
                engine.tick()

        except KeyboardInterrupt:
            self._close()

    def _receive(self):
        res = json.loads(self.ws.recv())

        self._seqnum(res['sequence'])

        if res.get('type') == 'match':
            self._callback('MATCH', res)
        elif res.get('type') == 'received':
            self._callback('RECEIVED', res)
        elif res.get('type') == 'open':
            self._callback('OPEN', res)
        elif res.get('type') == 'done':
            self._callback('DONE', res)
        elif res.get('type') == 'change':
            self._callback('CHANGE', res)
        else:
            self._callback('ERROR', res)

    def _close(self):
        print('Closing....')
        self.ws.close()

    def _seqnum(self, number: int):
        if self._lastseqnum == -1:
            # first seen
            self._lastseqnum = number
            return

        if number != self._lastseqnum + 1 and \
                number not in self._missingseqnum:
            print('ERROR: Missing sequence number/s: %s' % ','.join(
                str(x) for x in range(self._lastseqnum+1, number+1)))
            self._missingseqnum.update(
                x for x in range(self._lastseqnum+1, number+1))
            print(self._missingseqnum)

        if number in self._missingseqnum:
            self._missingseqnum.remove(number)
            print('INFO: Got out of order data for seqnum: %s' % number)

        else:
            self._lastseqnum = number

    def accountInfo(self):
        return self.client.getAccounts()

    def sendOrder(self, callback: Callback):
        '''send order to exchange'''

    def orderResponse(self, response):
        '''parse the response'''

    def buy(self, req: TradeRequest) -> ExecutionReport:
        '''execute a buy order'''

    def sell(self, req: TradeRequest) -> ExecutionReport:
        '''execute a sell order'''
