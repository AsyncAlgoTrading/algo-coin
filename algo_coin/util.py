
from enum import Enum, unique
from abc import ABCMeta, abstractmethod


@unique
class ExchangeType(Enum):
    coinbase = 1
    hitbtc = 2
    cryptsy = 3
    bitfinex = 4
    kraken = 5
    btce = 6

    @staticmethod
    def type(string):
        return ExchangeType[string]


class Endpoint(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_type(self):
        '''to be implemented'''

    @abstractmethod
    def APIInit(self):
        '''tp be implemented'''


class APIKey(object):
    def __init__(self, key, secret_key):
        self.key = key
        self.secret_key = secret_key

    def key(self):
        return self.key

    def secret_key(self):
        return self.secret_key

    def __str__(self):
        return self.key + "-" + self.secret_key

    def __repr__(self):
        return self.__str__()
