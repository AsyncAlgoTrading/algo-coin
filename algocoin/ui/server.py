import tornado.ioloop
import tornado.web
from .handlers.accounts import ServerAccountsHandler
from .handlers.messages import ServerMessagesHandler


class ServerHandler(tornado.web.RequestHandler):
    '''Server Handler
    Extends:
        tornado.web.RequestHandler
    '''
    def get(self):
        self.write("Server<br>")
        self.write('<a href="/api/json/v1/accounts">accounts</a><br>')
        self.write('<a href="/api/json/v1/messages">messages</a><br>')


class ServerApplication(tornado.web.Application):
    def __init__(self, trading_engine, *args, **kwargs):
        super(ServerApplication, self).__init__([
            (r"/", ServerHandler),
            (r"/api/json/v1/accounts", ServerAccountsHandler, {'trading_engine': trading_engine}),
            (r"/api/json/v1/messages", ServerMessagesHandler, {'trading_engine': trading_engine}),
        ])
