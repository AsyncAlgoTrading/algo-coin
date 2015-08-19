
from algo_coin.endpoint.endpoint import *
from abc import abstractmethod


class Exchange(Endpoint):
    def __init__(self, type):
        """ """
        super().__init__(type)

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def buy(self,):
        """ """
        pass

    @abstractmethod
    def sell(self):
        """ """
        pass


class ExchangeClient(object):
    def __init__(self, exchangeType, endpoint, exchangeClientProtocol):
        self.exchangeType = exchangeType
        self.endpoint = endpoint
        self.protocol = exchangeClientProtocol

    @abstractmethod
    def connectSocket(self, queue):
        """ """

    def run(self, queue):
        self.connectSocket(queue)
