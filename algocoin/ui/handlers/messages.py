import tornado.web
import ujson
from ...lib.enums import TickType, PairType


class ServerMessagesHandler(tornado.web.RequestHandler):
    '''Server Handler
    Extends:
        tornado.web.RequestHandler
    '''

    def initialize(self, trading_engine):
        self.te = trading_engine

    def get(self):
        try:
            type = self.get_argument('type', None)
            page = int(self.get_argument('page', 0))
            pairtype = self.get_argument('pair', '')

            try:
                type = TickType(type)
            except ValueError:
                pass
            try:
                pairtype = PairType.from_string(pairtype)
            except ValueError:
                pass

            if type is None:
                if pairtype:
                    msgs = self.te._ex.messages(False, pairtype)[-(page+1)*20: -1 + (page)*20] if page > 0 else self.te._ex.messages(False, pairtype)
                else:
                    msgs = self.te._ex.messages()[-(page+1)*20: -1 + (page)*20] if page > 0 else self.te._ex.messages()
            else:
                if pairtype:
                    msgs = self.te._ex.messages(True, pairtype).get(type, [])[page*20: (page+1)*20] if page > 0 else self.te._ex.messages(True, pairtype).get(type, [])
                else:
                    msgs = self.te._ex.messages(True).get(type, [])[page*20: (page+1)*20] if page > 0 else self.te._ex.messages(True).get(type, [])

            msgs = [x.to_dict(True, True) for x in msgs]

            self.write(ujson.dumps(msgs))
        except Exception as e:
            self.write(e)
