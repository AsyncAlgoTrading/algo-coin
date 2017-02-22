from typing import Callable
from abc import ABCMeta, abstractmethod
from .callback import Callback
from .structs import MarketData, TradeRequest, TradeResponse


def ticks(f):
    def wrapper(self, *args, **kwargs):
        self._tick = f(self, *args, **kwargs)
    return wrapper


class Strategy(metaclass=ABCMeta):
    '''Strategy interface'''
    def __init__(self, *args, **kwargs):
        self._tick = False
        self._actions = []
        self._requests = []

    def ticked(self):
        return self._tick

    def reset(self):
        self._tick = False

    def setEngine(self, engine):
        self._te = engine

    @abstractmethod
    def requestBuy(self,
                   callback: Callback,
                   data: MarketData):
        '''requestBuy'''

    @abstractmethod
    def requestSell(self,
                    callback: Callback,
                    data: MarketData):
        '''requestSell'''

    def registerAction(self, time, actionType, data):
        '''add action to log'''
        self._actions.append((time, actionType, data))

    def registerDesire(self, time, actionType, data):
        '''add action to log'''
        self._requests.append((time, actionType, data))


class TradingStrategy(Strategy, Callback):
    def requestBuy(self,
                   callback: Callable,
                   req: TradeRequest,
                   callback_failure=None):
        self._te.requestBuy(callback, req, callback_failure, self)

    def requestSell(self,
                    callback: Callable,
                    req: TradeRequest,
                    callback_failure=None):
        self._te.requestSell(callback, req, callback_failure, self)

    def slippage(self, data: TradeResponse):
        '''slippage model. default is pass through'''
        return data

    def transactionCost(self, data: TradeResponse):
        '''txns cost model. default is pass through'''
        return data
