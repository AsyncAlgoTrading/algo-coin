
from autobahn.twisted.websocket import WebSocketClientFactory,  \
    WebSocketClientProtocol, connectWS
from twisted.python import log as tp_log
from twisted.internet import reactor
import json
from algo_coin.exchange.core import ExchangeClient
from algo_coin.endpoint.endpoint import EndpointType
# import sys


class CoinbaseExchangeClientProtocol(WebSocketClientProtocol):
    def onConnect(self):
        #TODO
        self.log.write("here")
        pass

    def onOpen(self):
        self.log.write("here2")
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


class CoinbaseWebSocketClientFactory(WebSocketClientFactory):
    def __init__(self, string, queue, debug=True):
        super().__init__(string, debug)
        self.protocol = CoinbaseExchangeClientProtocol
        self.queue = queue
        CoinbaseExchangeClientProtocol.queue = queue


class CoinbaseExchangeClient(ExchangeClient):
    def __init__(self, endpoint, feed_handler, log):
        super(CoinbaseExchangeClient, self).__init__(
            EndpointType.type("coinbase"),
            endpoint, CoinbaseExchangeClientProtocol)
        self.log = log
        self.feed_handler = feed_handler

    def connect_socket(self, queue):
        tp_log.startLogging(self.log)
        factory = CoinbaseWebSocketClientFactory(
            "wss://ws-feed.exchange.coinbase.com",
            queue,
            debug=False)

        # factory2 = CoinbaseWebSocketClientFactory(
        #     "wss://ws-feed.exchange.coinbase.com",
        #     queue,
        #     debug=True)

        connectWS(factory)
        # connectWS(factory2)
        print(factory.queue)
        reactor.run(1)
        self.log.write("\n\n3\n\n")
