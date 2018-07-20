import os
import os.path
import logging
import tornado.ioloop
import tornado.web
from .handlers.accounts import ServerAccountsHandler
from .handlers.messages import ServerMessagesHandler
from .handlers.html import HTMLOpenHandler


class ServerApplication(tornado.web.Application):
    def __init__(self, trading_engine, debug=True, cookie_secret=None, *args, **kwargs):
        root = os.path.join(os.path.dirname(__file__), 'assets')
        static = os.path.join(root, 'static')

        logging.getLogger('tornado.access').disabled = True

        settings = {
                "cookie_secret": cookie_secret or "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",  # TODO
                "login_url": "/login",
                "debug": debug,
                "template_path": os.path.join(root, 'templates'),
                }

        super(ServerApplication, self).__init__([
            (r"/", HTMLOpenHandler, {'template': 'index.html'}),
            (r"/api/json/v1/accounts", ServerAccountsHandler, {'trading_engine': trading_engine}),
            (r"/api/json/v1/messages", ServerMessagesHandler, {'trading_engine': trading_engine}),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static}),
            (r"/(.*)", HTMLOpenHandler, {'template': '404.html'})
        ], **settings)
