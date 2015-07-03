
from algo_coin.util import *
from abc import ABCMeta, abstractmethod


class API(object):
    def __init__(self, api_key):
        """ """
        self.api_key = api_key
        self.name = None

    @abstractmethod
    def APIInit(self):
        """to be implemented"""


class WalletAPI(API):
    __metaclass__ = ABCMeta

    def __init__(self, api_key):
        """ """
        super().__init__(api_key)

    @abstractmethod
    def deposit(self, source):
        """to be implemented"""

    @abstractmethod
    def withdraw(self, source):
        """to be implemented"""


class ExchangeAPI(API):
    __metaclass__ = ABCMeta

    def __init__(Self, api_key):
        """ """
        super().__init__(api_key)

    @abstractmethod
    def buy(self, amount):
        """to be implemented"""

    @abstractmethod
    def sell(self, amount):
        """to be implemented"""
