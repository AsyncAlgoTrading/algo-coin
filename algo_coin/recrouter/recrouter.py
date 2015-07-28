
from multiprocessing import Process


class ReceiverRouter(object):
    def __init__(self, conn_engine):
        conn_engine.init_processes()
        self.queues = conn_engine.queues
        # self.connectivity = Process(target=monitor_connections,
        #                             args=(conn_engine,))

    def run(self):
        # self.connectivity.start()
        pass

    def terminate(self):
        # self.connectivity.terminate()  # TODO
        pass

def monitor_connections(conn_engine):
    conn_engine.run_processes()
    while(True):
        if not conn_engine.monitor_connections():
            conn_engine.restart_down()


def terminate_connections(conn_engine):
    conn_engine.terminate()
