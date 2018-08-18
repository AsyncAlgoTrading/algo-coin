# from abc import ABCMeta
from .structs import Instrument
from .enums import Side
from heapq import heappush, heappop


class Book(object):
    def __init__(self, instrument: Instrument):
        self._instrument = instrument
        self._bid = []
        self._ask = []

    def push(self, order) -> None:
        if order.side == Side.BUY:
            heappush(self._bid, order)
        else:
            heappush(self._ask, order)

    def pop(self, order) -> None:
        pass

    def __str__(self) -> str:
        return str(self._instrument) + '->\n' + \
               'ask:\t' + '\n\t'.join([str(x.volume) + '\t@\t' + str(x.price) for x in sorted(self._ask, reverse=True)]) + \
               '\n\t=====================\n' + \
               'bid:\t' + '\n\t'.join([str(x.volume) + '\t@\t' + str(x.price) for x in sorted(self._bid, reverse=True)]) + '\n'

    def __repr__(self) -> str:
        return self.__str__()


# class OrderBook(metaclass=ABCMeta):
class OrderBook(object):
    '''OrderBook interface'''
    def __init__(self, instruments):
        self._ob = {instrument: Book(instrument) for instrument in instruments}

    def preload(self, orders) -> None:
        pass

    def push(self, order) -> None:
        self._ob[order.instrument].push(order)

    def tob(self) -> list:
        return self._ob

    def __str__(self) -> str:
        return '\n\n'.join([str(self._ob[b]) for b in self._ob])

    def __repr__(self) -> str:
        return self.__str__()
