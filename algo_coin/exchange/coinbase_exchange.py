
from autobahn.twisted.websocket import WebSocketClientFactory,  \
    WebSocketClientProtocol, connectWS
from twisted.python import log as tp_log
from twisted.internet import reactor
import json
from algo_coin.exchange.core import ExchangeClient
from algo_coin.endpoint.endpoint import EndpointType
# import sys


class CoinbaseExchangeClientProtocol(WebSocketClientProtocol):
    queue = None

    def onConnect(self):
        #TODO
        print(self.queue)
        pass

    def onOpen(self):
        msg = json.dumps({"type": "subscribe", "product_id": "BTC-USD"})
        res = self.sendMessage(msg.encode('utf-8'), isBinary=False)
        print(res)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = json.loads(payload.decode('utf8'))
            print(msg)
            #pprint(msg)

    def onClose(self, wasClean, core, reason):
        #TODO
        pass


class CoinbaseExchangeClient(ExchangeClient):
    def __init__(self, endpoint, log):
        super(CoinbaseExchangeClient, self).__init__(
            EndpointType.type("coinbase"),
            endpoint, CoinbaseExchangeClientProtocol)
        self.log = log

    def connectSocket(self, queue):
        tp_log.startLogging(self.log)
        factory = WebSocketClientFactory("wss://ws-feed.exchange.coinbase.com",
                                         debug=True)
        factory.protocol = CoinbaseExchangeClientProtocol
        connectWS(factory)
        reactor.run()
