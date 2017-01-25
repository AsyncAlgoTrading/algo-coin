from callback import Callback
from config import BacktestConfig
from data_source import StreamingDataSource
from log import LOG as log


class Backtest(StreamingDataSource):
    def __init__(self, options: BacktestConfig):

        super(Backtest, self).__init__()
        self._file = options.file

    def run(self, engine):
        log.info('Starting....')
        with open(self._file, 'r') as fp:
            for line in fp:
                self._receive(line)
                engine.tick()
        self._callback('ANALYZE', None)

    def _receive(self,
                 line: str):
        res = line.strip().split(',')

        # TODO allow if market data for bid/ask
        res = {'type': 'match',
               'time': res[0],
               'price': res[1],
               'volume': res[2]}

        if res.get('type') == 'match':
            self._callback('MATCH', res)
        # elif res.get('type') == 'received':
        #     self._callback('RECEIVED', res)
        # elif res.get('type') == 'open':
        #     self._callback('OPEN', res)
        # elif res.get('type') == 'done':
        #     self._callback('DONE', res)
        # elif res.get('type') == 'change':
        #     self._callback('CHANGE', res)
        else:
            self._callback('ERROR', res)

    def _callback(self,
                  field: str,
                  data):
        for cb in self._callbacks[field]:
            cb(data)

    def onMatch(self,
                callback: Callback):
        self._callbacks['MATCH'].append(callback)

    def onReceived(self,
                   callback: Callback):
        self._callbacks['RECEIVED'].append(callback)

    def onOpen(self,
               callback: Callback):
        self._callbacks['OPEN'].append(callback)

    def onDone(self,
               callback: Callback):
        self._callbacks['DONE'].append(callback)

    def onChange(self,
                 callback: Callback):
        self._callbacks['CHANGE'].append(callback)

    def onError(self,
                callback: Callback):
        self._callbacks['ERROR'].append(callback)

    def onAnalyze(self,
                  callback: Callback):
        self._callbacks['ANALYZE'].append(callback)

    def onHalt(self,
               callback: Callback):
        self._callbacks['HALT'].append(callback)

    def onContinue(self,
                   callback: Callback):
        self._callbacks['CONTINUE'].append(callback)

    def registerCallback(self,
                         callback: Callback):
        if not isinstance(callback, Callback):
            raise Exception('%s is not an instance of class '
                            'Callback' % callback)

        if callback.onMatch:
            self.onMatch(callback.onMatch)
        if callback.onAnalyze:
            self.onAnalyze(callback.onAnalyze)
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
        if callback.onHalt:
            self.onHalt(callback.onHalt)
        if callback.onContinue:
            self.onContinue(callback.onContinue)
