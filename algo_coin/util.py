
from enum import Enum, unique
from abc import ABCMeta, abstractmethod
from dateutil import parser


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
        """ """
        return ExchangeType[string]


class Endpoint(object):
    __metaclass__ = ABCMeta

    def __init__(self, type):
        """ """
        if not isinstance(type, ExchangeType):
            raise TypeError
        self.type = type

    def get_type(self):
        """ """
        return self.type

    @abstractmethod
    def APIInit(self, api_key):
        '''tp be implemented'''


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
