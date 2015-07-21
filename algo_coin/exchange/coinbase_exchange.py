
from autobahn.twisted.websocket import WebSocketClientFactory,  \
    WebSocketClientProtocol, connectWS
#from twisted.python import log
from twisted.internet import reactor
import json
from . import ExchangeClient
from algo_coin.util.util import ExchangeType


class CoinbaseExchangeClientProtocol(WebSocketClientProtocol):

    def onConnect(self):
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
        pass


class CoinbaseExchangeClient(ExchangeClient):
    def __init__(self, endpoint):
        self.super(ExchangeType.type("coinbase"), endpoint,
                   CoinbaseExchangeClientProtocol)
        self.super()

    def connectSocket(self):
        #log.startLogging(sys.stdout)
        factory = WebSocketClientFactory("wss://ws-feed.exchange.coinbase.com",
                                         debug=True)
        factory.protocol = CoinbaseExchangeClientProtocol
        connectWS(factory)
        reactor.run()
