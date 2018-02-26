import tornado.ioloop
import tornado.web
import ujson


class ServerHandler(tornado.web.RequestHandler):
    '''Server Handler
    Extends:
        tornado.web.RequestHandler
    '''
    def get(self):
        self.write("Server<br>")
        self.write('<a href="/accounts">accounts</a>')


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


class ServerApplication(tornado.web.Application):
    def __init__(self, trading_engine, *args, **kwargs):
        super(ServerApplication, self).__init__([
            (r"/", ServerHandler),
            (r"/accounts", ServerAccountsHandler, {'trading_engine': trading_engine}),
        ])
