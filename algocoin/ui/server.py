import os
import os.path
import tornado.ioloop
import tornado.web
from aat.ui.handlers.html import HTMLHandler, HTMLOpenHandler


def getHandlers():
    root = os.path.join(os.path.dirname(__file__), 'assets')
    static = os.path.join(root, 'static')

    settings = {
        "template_path": os.path.join(root, 'templates'),
    }

    return settings, [
        (r"/", HTMLHandler, {'template': 'index.html'}),
        (r"/login", HTMLOpenHandler, {'template': 'login.html'}),
        (r"/logout", HTMLHandler, {'template': 'logout.html'}),
        (r"/static/js/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(static, 'js')}),
        (r"/static/css/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(static, 'css')}),
        (r"/static/fonts/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(static, 'fonts')}),
        ]
