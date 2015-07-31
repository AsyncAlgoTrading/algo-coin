
from multiprocessing import Process
import time

s_name = "ReceiverRouter"


class ReceiverRouter(object):
    def __init__(self, queues, log):
        self.queues = queues
        self.recrouter = Process(target=deploy_rr,
                                 args=[self])
        self.log = log

    def select(self):
        pass

    def run(self):
        self.recrouter.start()

    def terminate(self):
        print("ReceiverRouter going down")
        if self.recrouter.is_alive():
            self.recrouter.terminate()
        self.recrouter.join()


def deploy_rr(recrouter):
    while(True):
        time.sleep(1)
        continue
    pass
