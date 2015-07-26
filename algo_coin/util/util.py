
from enum import Enum, unique
from abc import ABCMeta, abstractmethod
from dateutil import parser


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


class APIKey(object):
    def __init__(self, key, secret_key):
        """ """
        self.key = key
        self.secret_key = secret_key

    def get_key(self):
        """ """
        return self.key

    def get_secret_key(self):
        """ """
        return self.secret_key

    def __str__(self):
        """ """
        return self.key + "-" + self.secret_key

    def __repr__(self):
        """ """
        return self.__str__()


def ConvertTime(json_time):
    return parser.parse(json_time)


def insertPythonTime(return_json):
    for row in return_json:
        if type(row) is dict:
            if "time" in row.keys():
                row['python_time'] = ConvertTime(row['time'])
    return return_json


"""This is the reconstructed book for an individual exchange"""
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

"""Class maintains the user's outstanding orders across all exchanges"""
class UserOrderBook(object):
    def __init__():
        pass
