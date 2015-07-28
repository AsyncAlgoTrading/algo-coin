
from multiprocessing import Process, Queue


class ConnectivityEngine(object):
    def __init__(self, conn_manager):
        self.processes = {}
        self.queues = {}
        self.down = []
        print("active:" + str(conn_manager.get_active()))
        self.active = conn_manager.get_active()
        self.exchanges = conn_manager.get_exchanges()

    def init_processes(self):
        for end in self.active:
            self.queues[end] = Queue()
            self.processes[end] = Process(target=run,
                                          args=(self.exchanges[end],
                                          self.queues[end]))

    def run_processes(self):
        for end in self.active:
            self.processes[end].start()

    def monitor_processes(self):
        for end in self.active:
            if not self.processes[end].is_alive():
                self.down.append(end)
        print (self.down)
        return len(self.down) == 0

    def restart_down(self):
        for end in self.down:
            self.processes[end] = Process(target=run,
                                          args=(self.exchanges[end],
                                          self.queues[end]))
            self.processes[end].start()
        self.down = []

    def terminate(self):
        print("ConnectivityEngine going down")
        for k in self.processes.keys():
            if self.processes[k].is_alive():
                self.processes[k].terminate()
            self.processes[k].join()

def run(exchange, queue):
    exchange.run(queue)
