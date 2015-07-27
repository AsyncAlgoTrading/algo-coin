
from enum import Enum, unique
from abc import ABCMeta, abstractmethod


@unique
class EndpointType(Enum):
    coinbase = 1
    hitbtc = 2
    cryptsy = 3
    bitfinex = 4
    kraken = 5
    btce = 6

    @staticmethod
    def type(string):
        """ """
        return EndpointType[string]


class Endpoint(object):
    __metaclass__ = ABCMeta

    def __init__(self, type):
        """ """
        if not isinstance(type, EndpointType):
            raise TypeError
        self.type = type

    def get_type(self):
        """ """
        return self.type

    @abstractmethod
    def APIInit(self, api_key):
        '''to be implemented'''

    @abstractmethod
    def run(self):
        """to be implemented"""

    @abstractmethod
    def heartbeat(self):
        """to be implemented """
