

'''RecRouter is going to have one "channel" for each
exchange, where messages from that exchange are sent

then it routes the messages to both the exchange orderbook
and the global orderbook, as well as the strategy manager
'''


class ReceiverRouter(object):
    def __init__(self, log):
        """ """
        self.http_endpoints = []  # possible input channels
        self.websockets = []  # possible input channels
        self.log = log
        pass

    def register(self, in_channel, type):
        ''' type->http or websocket
        '''
        pass

    def unregister(self, in_channel, type):
        '''type->http or websocket'''
