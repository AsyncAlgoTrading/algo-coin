from abc import ABCMeta, abstractmethod
from .callback import Callback, NullCallback
from .structs import MarketData
from .enums import Side


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


class TradingStrategy(Strategy, Callback):
    def requestBuy(self,
                   callback: Callback,
                   data: MarketData,
                   callback_failure=None):
        self._te.requestBuy(callback, data, callback_failure)

    def requestSell(self,
                    callback: Callback,
                    data: MarketData,
                    callback_failure=None):
        self._te.requestSell(callback, data, callback_failure)


class NullTradingStrategy(Strategy, NullCallback):
    def requestBuy(self,
                   callback: Callback,
                   data: MarketData,
                   callback_failure=None):
        # let them do whatever
        self.registerAction(data.time, Side.BUY, data.price)
        callback(data)

    def requestSell(self,
                    callback: Callback,
                    data: MarketData,
                    callback_failure=None):
        # let them do whatever
        self.registerAction(data.time, Side.SELL, data.price)
        callback(data)


class BacktestTradingStrategy(NullTradingStrategy):
    # TODO data should be txn req not dict
    def slippage(self, data):
        '''slippage model. default is pass through'''
        return data

    # TODO data should be txn req not dict
    def transactionCost(self, data):
        '''txns cost model. default is pass through'''
        return data

    def requestBuy(self,
                   callback: Callback,
                   data: MarketData,
                   callback_failure=None):
        # let them do whatever
        data = self.transactionCost(self.slippage(data))
        self.registerAction(data.time, Side.BUY, data.price)
        callback(data)

    def requestSell(self,
                    callback: Callback,
                    data: MarketData,
                    callback_failure=None):
        # let them do whatever
        data = self.transactionCost(self.slippage(data))
        self.registerAction(data.time, Side.SELL, data.price)
        callback(data)
