from websocket import create_connection
import json
from callback import Callback


class Exchange(object):
    def __init__(self, sandbox=False):
        self._callbacks = {'MATCH': [],
                           'RECEIVED': [],
                           'ERROR': [],
                           'OPEN': [],
                           'DONE': [],
                           'CHANGE': []}
        self._lastseqnum = -1
        self._missingseqnum = set()

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

    def _seqnum(self, number):
        if self._lastseqnum == -1:
            # first seen
            self._lastseqnum = number
            return

        if number in self._missingseqnum:
            self._missingseqnum.remove(number)
            print('INFO: Got out of order data for seqnum: %s' % number)

        elif number != self._lastseqnum + 1:
            print('ERROR: Missing sequence number/s: %s' % ','.join(
                str(x) for x in range(self._lastseqnum+1, number+1)))
            self._missingseqnum.add(
                x for x in range(self._lastseqnum+1, number+1))

        else:
            self._lastseqnum = number

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

    def _callback(self, field, data):
        for cb in self._callbacks[field]:
            cb(data)

    def onMatch(self, callback):
        self._callbacks['MATCH'].append(callback)

    def onReceived(self, callback):
        self._callbacks['RECEIVED'].append(callback)

    def onOpen(self, callback):
        self._callbacks['OPEN'].append(callback)

    def onDone(self, callback):
        self._callbacks['DONE'].append(callback)

    def onChange(self, callback):
        self._callbacks['CHANGE'].append(callback)

    def onError(self, callback):
        self._callbacks['ERROR'].append(callback)

    def registerCallback(self, callback):
        if not isinstance(callback, Callback):
            raise Exception('%s is not an instance of class '
                            'Callback' % callback)

        if callback.onMatch:
            self.onMatch(callback.onMatch)
        if callback.onReceived:
            self.onReceived(callback.onReceived)
        if callback.onOpen:
            self.onOpen(callback.onOpen)
        if callback.onDone:
            self.onDone(callback.onDone)
        if callback.onChange:
            self.onChange(callback.onChange)
        if callback.onError:
            self.onError(callback.onError)
