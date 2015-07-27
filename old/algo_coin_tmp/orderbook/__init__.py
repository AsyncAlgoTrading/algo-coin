
from algo_coin.orderbook.core import *

from enum import Enum, unique


@unique
class OrderType(Enum):
    buy = 1
    sell = 2

    @staticmethod
    def type(string):
        """ """
        return OrderType[string]
