import sys
import time

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory, connectWS
from twisted.python import log
from twisted.internet import reactor

from multiprocessing import Queue, Process


def run(*args):
    log.startLogging(sys.stdout)

    #Construct Socket
    active = ['coinbase']
    endpoints = {'coinbase': 'wss://ws-feed.exchange.coinbase.com'}

    print(active)

    factory = CoinbaseClientFactory(endpoints['coinbase'], debug=True)
    queue = factory.protocol.queue
    print(factory.protocol.queue)
    socket_process = Process(target=run_reactor, args=(factory,))

    #Construct Strategy
    stategy = EchoStrategy()
    stategy_process = Process(target=stategy.run, args=(queue,))

    #plug callback handler into strategy and socket
    #
    # Eventually, instead of socket talking directly
    # to a strategy, we use the RecRouter to aggregate
    # socket messages, and use the SendEng to
    # aggregate Strategy messages.
    #

    #connect all
    try:
        socket_process.start()
        stategy_process.start()

        #monitor threads and killall if they die
        time.sleep(25)

    except KeyboardInterrupt:
        # if(socket_process.is_alive()):
        # socket_process.terminate()
        socket_process.join()
        # if(stategy_process.is_alive()):
        # stategy_process.terminate()
        stategy_process.join()


class CoinbaseExchangeClientProtocol(WebSocketClientProtocol):
    queue = Queue()

    def onConnect(self):
        pass

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        pass

    def onClose(self, wasClean, core, reason):
        pass


class CoinbaseClientFactory(WebSocketClientFactory):
    protocol = CoinbaseExchangeClientProtocol

    def clientConnectionLost(self, connector, reason):
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        reactor.stop()


class EchoStrategy(object):
    def __init__(self):
        pass

    def newInfo(self, msg):
        print(msg)

    def run(self, queue):
        self.queue = queue
        print(self.queue)
        while(True):
            time.sleep(5)
            print("STRAT-HB")


def run_reactor(factory):
    connectWS(factory)
    reactor.run()
    return


if __name__ == "__main__":
    run(sys.argv)
