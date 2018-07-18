import tornado.web
import ujson
from datetime import datetime
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

            try:
                type = TickType(type)
            except ValueError:
                pass

            msgs = self.te._ex.messages()
            msgs = {str(a): [x.to_dict() for x in msgs[a]] for a in msgs if type is None or a == type}

            # convert to str
            for k in msgs:
                for v in msgs[k]:
                    for kk in v:
                        if isinstance(v[kk], datetime):
                            v[kk] = v[kk].strftime('%d/%m/%y %H:%M:%S')
                        else:
                            v[kk] = str(v[kk])

            self.write(ujson.dumps(msgs))
        except Exception as e:
            self.write(e)
