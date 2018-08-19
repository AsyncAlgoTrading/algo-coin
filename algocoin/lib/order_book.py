# from abc import ABCMeta
from .structs import Instrument
from .enums import Side, TickType
from heapq import heappush, heappop


class Order(object):
    def __init__(self, price, volume):
        self.price = price
        self.volume = volume

    def __lt__(self, other):
        return self.price < other.price


class Book(object):
    def __init__(self, instrument: Instrument):
        self._instrument = instrument
        self._bid = []
        self._bidd = {}

        self._ask = []
        self._askk = {}

    def push(self, order) -> None:
        if order.side == Side.BUY:
            if order.type == TickType.DONE:
                if order.price not in self._bidd:
                    pass
                else:
                    self._bidd[order.price].volume -= order.volume
                    if self._bidd[order.price].volume < 1e-5:
                        self._bid.remove(self._bidd[order.price])
                        del self._bidd[order.price]

            elif order.type == TickType.CHANGE:
                if order.price not in self._bidd:
                    pass
                else:
                    self._bidd[order.price].volume -= order.volume
                    if self._bidd[order.price].volume < 1e-5:
                        self._bid.remove(self._bidd[order.price])
                        del self._bidd[order.price]

            elif order.type == TickType.OPEN:
                if order.price in self._bidd:
                    self._bidd[order.price].volume += order.volume
                else:
                    self._bid.append(Order(order.price, order.volume))
                    self._bidd[order.price] = self._bid[-1]
            else:
                self._bid.append(Order(order.price, order.volume))
                self._bidd[order.price] = self._bid[-1]
        else:
            if order.type == TickType.DONE:
                if order.price not in self._askk:
                    pass
                else:
                    self._askk[order.price].volume -= order.volume
                    if self._askk[order.price].volume < 1e-5:
                        self._ask.remove(self._askk[order.price])
                        del self._askk[order.price]

            elif order.type == TickType.CHANGE:
                if order.price not in self._askk:
                    pass
                else:
                    self._askk[order.price].volume -= order.volume
                    if self._askk[order.price].volume < 1e-5:
                        self._ask.remove(self._askk[order.price])
                        del self._askk[order.price]

            elif order.type == TickType.OPEN:
                if order.price in self._askk:
                    self._askk[order.price].volume += order.volume
                else:
                    self._ask.append(Order(order.price, order.volume))
                    self._askk[order.price] = self._ask[-1]

            else:
                self._ask.append(Order(order.price, order.volume))
                self._askk[order.price] = self._ask[-1]

    def pop(self, order) -> None:
        pass

    def __str__(self) -> str:
        return str(self._instrument) + '->\n' + \
               'ask:\t' + '\n\t'.join(['%.1f\t@\t%.1f' % (x.volume, x.price) for x in sorted(self._ask, reverse=True)]) + \
               '\n\t=====================\n' + \
               'bid:\t' + '\n\t'.join(['%.1f\t@\t%.1f' % (x.volume, x.price) for x in sorted(self._bid, reverse=True)]) + '\n'

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
