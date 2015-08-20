
from autobahn.twisted.websocket import WebSocketClientProtocol
import json
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

    def __repr__(self):
        return "CoinbaseExchangeClientProtocol"

    def __str__(self):
        return self.__repr__()
