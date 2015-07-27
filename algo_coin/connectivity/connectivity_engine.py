
from multiprocessing import Process, Queue


class ConnectivityEngine(object):
    def __init__(self, conn_manager):
        self.processes = {}
        self.queues = {}
        self.down = []
        print(conn_manager.get_active())
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
            if not self.processes[end].is_running():
                self.down.append(end)
        return len(self.down) == 0

    def restart_down(self):
        for end in self.down:
            self.processes[end] = Process(target=run,
                                          args=(self.exchanges[end],))
            self.processes[end].start()
        self.down = []


def run(exchange, queue):
    exchange.run(queue)
