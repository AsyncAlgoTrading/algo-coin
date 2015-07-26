
from multiprocessing import Process
# from algo_coin.dashboard import dashboard as db
from algo_coin.connectivity import connectivity_engine as ce
from algo_coin.util.log import *


class DashboardProcess(Process):
    def __init__(self,):
        Process.__init__(self)
        # self.queue = q

    def start(self):
        self.queue.put_nowait(1)

    def restart(self):
        pass

    def terminate(self):
        pass


def ConnectivityProcess(Process):
    def __init__(self, args):
        Process.__init__(self)
        # self.queue = q
        self.ce = ce.ConnectivityEngine(Log())
        self.args = args

    def start(self):
        ce.setup(self.args[0], self.args[1], self.args[2])
        self.queue.put_nowait(1)

    def restart(self):
        pass

    def terminate(self):
        pass
