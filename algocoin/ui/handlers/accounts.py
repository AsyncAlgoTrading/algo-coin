import tornado.web
import ujson


class ServerAccountsHandler(tornado.web.RequestHandler):
    '''Server Handler
    Extends:
        tornado.web.RequestHandler
    '''

    def initialize(self, trading_engine):
        self.te = trading_engine

    def get(self):
        try:
            self.write(ujson.dumps([a.to_dict() for a in self.te._ex.accounts()]))
        except Exception as e:
            self.write(e)
