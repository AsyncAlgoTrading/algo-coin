from callback import Callback, NullCallback
from abc import ABCMeta, abstractmethod
from datetime import datetime


def ticks(f):
    def wrapper(self, *args, **kwargs):
        self._tick = f(self, *args, **kwargs)
    return wrapper


class Strategy(metaclass=ABCMeta):
    '''Strategy interface'''
    def __init__(self, *args, **kwargs):
        self._tick = False
        self._actions = []

    def ticked(self):
        return self._tick

    def reset(self):
        self._tick = False

    @abstractmethod
    def requestBuy(self, callback, data):
        '''requestBuy'''

    @abstractmethod
    def requestSell(self, callback, data):
        '''requestSell'''


class TradingStrategy(Strategy, Callback):
    def callback(self):
        return self

    def requestBuy(self, callback, data):
        self._te.requestBuy(data)

    def requestSell(self, callback, data):
        self._te.requestBuy(data)


class NullTradingStrategy(Strategy, NullCallback):
    def callback(self):
        return self

    def requestBuy(self, callback, data):
        self._actions.append((datetime.fromtimestamp(float(data['time'])),
                              'buy',
                              data['price']))
        # let them do whatever
        callback(data)

    def requestSell(self, callback, data):
        # let them do whatever
        self._actions.append((datetime.fromtimestamp(float(data['time'])),
                              'sell',
                              data['price']))
        callback(data)
