# import json
from abc import ABCMeta, abstractmethod
from callback import Callback
# from structs import MarketData


class DataSource(metaclass=ABCMeta):
    pass


class RestAPIDataSource(DataSource):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def sendOrder(self, callback: Callback):
        '''send order to exchange'''


class StreamingDataSource(DataSource):
    def __init__(self, *args, **kwargs):
        self._callbacks = {'MATCH': [],
                           'RECEIVED': [],
                           'ERROR': [],
                           'OPEN': [],
                           'DONE': [],
                           'CHANGE': [],
                           'ANALYZE': []}

    def run(self, engine):
        '''run the exchange'''

    def onMatch(self, callback: Callback):
        self._callbacks['MATCH'].append(callback)

    def onReceived(self, callback: Callback):
        self._callbacks['RECEIVED'].append(callback)

    def onOpen(self, callback: Callback):
        self._callbacks['OPEN'].append(callback)

    def onDone(self, callback: Callback):
        self._callbacks['DONE'].append(callback)

    def onChange(self, callback: Callback):
        self._callbacks['CHANGE'].append(callback)

    def onError(self, callback: Callback):
        self._callbacks['ERROR'].append(callback)

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
