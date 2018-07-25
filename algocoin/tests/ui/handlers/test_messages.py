import tornado.web
import os.path
from ....ui.handlers.messages import ServerMessagesMixin, ServerMessagesHandler, ServerMessagesWSHandler
from mock import MagicMock
import tornado.websocket


class TestMessages:
    def setup(self):
        settings = {
                "debug": "True",
                "template_path": os.path.join(os.path.dirname(__file__), '../', '../', 'ui', 'assets', 'templates'),
                }
        self.app = tornado.web.Application(**settings)
        self.app._transforms = []

    def test_ServerMessagesMixin(self):
        req = MagicMock()
        req.body = ''
        x = ServerMessagesMixin()
        x._transforms = []
        # x.get()
