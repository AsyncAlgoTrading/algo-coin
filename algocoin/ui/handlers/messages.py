import tornado.web
import tornado.websocket
import ujson
from ...lib.enums import TickType, PairType
from ...lib.structs import Instrument


class ServerMessagesMixin(object):
    def get_data(self, type=None, page=0, pairtype=None):
        try:
            type = TickType(type)
        except ValueError:
            type = None

        try:
            pairtype = PairType.from_string(pairtype)
            instrument = Instrument(underlying=pairtype)
        except (ValueError, TypeError):
            instrument = None

        if type is None:
            if instrument:
                msgs = self.te._ex.messages(False, instrument)[-(page+1)*20: -1 + (page)*20] if page > 0 else self.te._ex.messages(False, instrument)
            else:
                msgs = self.te._ex.messages()[-(page+1)*20: -1 + (page)*20] if page > 0 else self.te._ex.messages()
        else:
            if instrument:
                msgs = self.te._ex.messages(True, instrument).get(type, [])[page*20: (page+1)*20] if page > 0 else self.te._ex.messages(True, instrument).get(type, [])
            else:
                msgs = self.te._ex.messages(True).get(type, [])[page*20: (page+1)*20] if page > 0 else self.te._ex.messages(True).get(type, [])
        msgs = [x.to_dict(True, True) for x in msgs]

        if len(msgs) > 0:
            for msg in msgs:
                msg['underlying'] = msg['instrument']['underlying']
        return msgs


class ServerMessagesHandler(ServerMessagesMixin, tornado.web.RequestHandler):
    '''Server Handler
    Extends:
        tornado.web.RequestHandler
    '''

    def initialize(self, trading_engine):
        self.te = trading_engine

    def get(self):
        type = self.get_argument('type', None)
        page = int(self.get_argument('page', 0))
        pairtype = self.get_argument('pair', '')
        msgs = self.get_data(type, page, pairtype)
        self.write(ujson.dumps({'data': msgs}))


class ServerMessagesWSHandler(ServerMessagesMixin, tornado.web.RequestHandler):
    '''Server Handler
    Extends:
        tornado.web.RequestHandler
    '''

    def initialize(self, trading_engine):
        self.te = trading_engine

    def open(self):
        print('ws opened')

    def on_message(self, message):
        type = self.get_argument('type', None)
        page = int(self.get_argument('page', 0))
        pairtype = self.get_argument('pair', '')

        # TODO if page <0, stream
        msgs = self.get_data(type, page, pairtype)
        self.write_message(ujson.dumps(msgs))

    def on_close(self):
        pass
