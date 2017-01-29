# import json
from abc import ABCMeta, abstractmethod
from .callback import Callback
from .structs import TradeRequest, TradeResponse, ExecutionReport
from .enums import TickType
# from structs import MarketData


class DataSource(metaclass=ABCMeta):
    pass


class RestAPIDataSource(DataSource):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def sendOrder(self, callback: Callback):
        '''send order to exchange'''

    @abstractmethod
    def orderResponse(self, response):
        '''parse the response'''

    @abstractmethod
    def buy(self, req: TradeRequest) -> ExecutionReport:
        '''execute a buy order'''

    @abstractmethod
    def sell(self, req: TradeRequest) -> ExecutionReport:
        '''execute a sell order'''


class StreamingDataSource(DataSource):
    def __init__(self, *args, **kwargs):
        self._callbacks = {TickType.MATCH: [],
                           TickType.RECEIVED: [],
                           TickType.ERROR: [],
                           TickType.OPEN: [],
                           TickType.DONE: [],
                           TickType.CHANGE: [],
                           TickType.ANALYZE: [],
                           TickType.HALT: [],
                           TickType.CONTINUE: []}

    @abstractmethod
    def run(self, engine):
        '''run the exchange'''

    def _callback(self, field: str, data):
        for cb in self._callbacks[field]:
            cb(data)

    def onMatch(self, callback: Callback):
        self._callbacks[TickType.MATCH].append(callback)

    def onReceived(self, callback: Callback):
        self._callbacks[TickType.RECEIVED].append(callback)

    def onOpen(self, callback: Callback):
        self._callbacks[TickType.OPEN].append(callback)

    def onDone(self, callback: Callback):
        self._callbacks[TickType.DONE].append(callback)

    def onChange(self, callback: Callback):
        self._callbacks[TickType.CHANGE].append(callback)

    def onError(self, callback: Callback):
        self._callbacks[TickType.ERROR].append(callback)

    def onAnalyze(self, callback: Callback):
        self._callbacks[TickType.ANALYZE].append(callback)

    def onHalt(self, callback: Callback):
        self._callbacks[TickType.HALT].append(callback)

    def onContinue(self, callback: Callback):
        self._callbacks[TickType.CONTINUE].append(callback)

    def registerCallback(self, callback: Callback):
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
        if callback.onAnalyze:
            self.onAnalyze(callback.onAnalyze)
        if callback.onHalt:
            self.onHalt(callback.onHalt)
        if callback.onContinue:
            self.onContinue(callback.onContinue)
