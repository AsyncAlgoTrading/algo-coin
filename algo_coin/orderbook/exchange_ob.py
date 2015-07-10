
"""This is the reconstructed book for an individual exchange"""

from abc import abstractmethod


class ExchangeOrderBook(object):
    def __init__(self, exchange_type):
        self.exchange_type = exchange_type
        pass

    @abstractmethod
    def buy_order(self):
        pass

    @abstractmethod
    def sell_order(self):
        pass

    @abstractmethod
    def order_fill(self):
        pass

    @abstractmethod
    def order_done(self):
        pass

    @abstractmethod
    def order_change(self):
        pass
