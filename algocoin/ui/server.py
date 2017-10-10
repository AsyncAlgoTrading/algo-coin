import tornado.ioloop
import tornado.web


class ServerHandler(tornado.web.RequestHandler):
    '''Server Handler
    Extends:
        tornado.web.RequestHandler
    '''
    def get(self):
        self.write("Server")


class ServerApplication(tornado.web.Application):
    def __init__(self, trading_engine, *args, **kwargs):
        super(ServerApplication, self).__init__([
            (r"/", ServerHandler),
        ])
