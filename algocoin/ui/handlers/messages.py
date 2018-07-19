import tornado.web
import ujson
from ...lib.enums import TickType


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

            try:
                type = TickType(type)
            except ValueError:
                pass

            if type is None:
                msgs = self.te._ex.messages()[-(page+1)*20: -1 + (page)*20] if page > 0 else self.te._ex.messages()
            else:
                msgs = self.te._ex.messages(True).get(type, [])[page*20: (page+1)*20] if page > 0 else self.te._ex.messages(True).get(type, [])

            msgs = [x.to_dict(True) for x in msgs]

            self.write(ujson.dumps(msgs))
        except Exception as e:
            self.write(e)
