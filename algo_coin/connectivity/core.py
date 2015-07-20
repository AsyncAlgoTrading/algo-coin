
from abc import abstractmethod


class ExchangeClient(object):
    def __init__(self, exchangeType):
        self.exchangeType = exchangeType

    @abstractmethod
    def connectSocket(self, endpoint):
        """Endpoint is the ip and path of the exchange websocket endpoint"""
