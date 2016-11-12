from callback import Callback, NullCallback
from abc import ABCMeta, abstractmethod
from utils import parseDate


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

    def requestBuy(self, callback, data, callback_failure=None):
        self._te.requestBuy(callback, data, callback_failure)

    def requestSell(self, callback, data, callback_failure=None):
        self._te.requestSell(callback, data, callback_failure)


class NullTradingStrategy(Strategy, NullCallback):
    def callback(self):
        return self

    def requestBuy(self, callback, data, callback_failure=None):
        # let them do whatever
        date = parseDate(data['time'])
        self._actions.append((date, 'buy', data['price']))
        callback(data)

    def requestSell(self, callback, data, callback_failure=None):
        # let them do whatever
        date = parseDate(data['time'])
        self._actions.append((date, 'sell', data['price']))
        callback(data)
