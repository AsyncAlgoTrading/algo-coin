
from algo_coin.util.util import *
from algo_coin.apis.coinbase_api import *

# from abc import abstractmethod
from autobahn.twisted.websocket import WebSocketClientFactory,  \
    connectWS
# from twisted.python import log
from twisted.internet import reactor
#from pprint import pprint
# import sys
# import json


class Exchange(Endpoint):
    def __init__(self, type):
        """ """
        super().__init__(type)

    def APIInit(self, api_key):
        """ """
        if self.type is ExchangeType.coinbase:
            self.exchange_api = CoinbaseExchangeAPI(api_key)

        self.exchange_api.APIInit()

    def buy(self,):
        """ """
        pass

    def sell(self):
        """ """
        pass


class ExchangeClient(object):
    def __init__(self, exchangeType, endpoint, exchangeClientProtocol):
        self.exchangeType = exchangeType
        self.endpoint = endpoint
        self.protocol = exchangeClientProtocol

    def connectSocket(self):
        #log.startLogging(sys.stdout)
        factory = WebSocketClientFactory(self.endpoint, debug=True)
        factory.protocol = self.protocol
        connectWS(factory)
        reactor.run()
