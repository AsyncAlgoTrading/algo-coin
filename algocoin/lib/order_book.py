# from abc import ABCMeta
from .structs import Instrument


# class OrderBook(metaclass=ABCMeta):
class OrderBook():
    '''OrderBook interface'''
    def __init__(self, instrument: Instrument):
        pass

    def preload(self, orders):
        pass


