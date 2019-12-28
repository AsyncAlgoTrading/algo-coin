import os
import os.path
import tornado.ioloop
import tornado.web
from tornado_sqlalchemy_login.handlers import BaseHandler


class HTMLHandler(BaseHandler):
    def initialize(self, template=None, basepath="/", wspath="/", **kwargs):
        super(HTMLHandler, self).initialize(template=template, basepath=basepath, wspath=wspath, **kwargs)

    def get(self, *args):
        '''Get the login page'''
        template = self.render_template(self.template)
        self.write(template)

def getHandlers():
    root = os.path.join(os.path.dirname(__file__), 'assets')
    static = os.path.join(root, 'static')

    settings = {
        "assets_path": root,
        "static_path": static,
    }

    return settings, [
        (r"/", HTMLHandler, {'template': 'index.html', 'template_dirs': [os.path.join(root, "templates")]}),
        (r"/index.html", HTMLHandler, {'template': 'index.html'}),
        (r"/static/js/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(static, 'js')}),
        (r"/static/css/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(static, 'css')}),
        (r"/static/fonts/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(static, 'fonts')}),
        (r"(.*)", HTMLHandler, {'template': '404.html', 'template_dirs': [os.path.join(root, "templates")]}),
    ]
