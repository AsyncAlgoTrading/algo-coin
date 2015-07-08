
from flask import Flask

s_name = "DASHBOARD"

app = Flask(__name__)


class Dashboard(object):
    def __init__(self, log):
        """Initialize with logfile"""
        self.log = log
        print(app)
        pass

    def c_connectivity_engine(self, ce):
        """Connect connectivity engine to dashboard"""
        self.ce = ce

    def c_receiver_router(self, rr):
        """Connect receiver router to dashboard"""
        self.rr = rr

    def c_send_engine(self, se):
        """Connect send engine to dashboard"""
        self.se = se

    def c_order_book(self, ob):
        """Connect order book to dashboard"""
        self.ob = ob

    def c_wallets(self, bk):
        """Connect bank to dashboard"""
        self.bk = bk

    def run(self):
        app.run()
