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
        try:
            date = datetime.fromtimestamp(float(data['time']))
        except ValueError:
            date = datetime.strptime(data['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        self._actions.append((date,'buy',data['price']))
        # let them do whatever
        callback(data)

    def requestSell(self, callback, data):
        # let them do whatever
        try:
            date = datetime.fromtimestamp(float(data['time']))
        except ValueError:
            date = datetime.strptime(data['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        self._actions.append((date,'sell',data['price']))
        # let them do whatever
        callback(data)
