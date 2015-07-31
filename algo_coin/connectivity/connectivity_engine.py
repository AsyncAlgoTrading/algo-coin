
from multiprocessing import Process, Queue

s_name = "ConnectionEngine"


class ConnectivityEngine(object):
    def __init__(self, conn_manager, log):
        self.log = log
        self.processes = {}
        self.queues = {}
        self.down = []
        print("active: " + str(conn_manager.get_active()))
        self.log.log(s_name, "Active: " + str(conn_manager.get_active()))
        self.active = conn_manager.get_active()
        self.exchanges = conn_manager.get_exchanges()

    def init_processes(self):
        for end in self.active:
            self.log.log(s_name, "Initializing process: " + end)
            self.queues[end] = Queue()
            self.processes[end] = Process(target=run,
                                          args=(self.exchanges[end],
                                          self.queues[end]))

    def run_processes(self):
        for end in self.active:
            self.log.log(s_name, "Running process:" + end)
            self.processes[end].start()

    def monitor_processes(self):
        for end in self.active:
            if not self.processes[end].is_alive():
                self.log.log(s_name, "Process Down: " + end)
                self.down.append(end)
        return len(self.down) == 0

    def restart_down(self):
        for end in self.down:
            self.log.log(s_name, "Restarting: " + end)
            self.processes[end] = Process(target=run,
                                          args=(self.exchanges[end],
                                          self.queues[end]))
            self.processes[end].start()
        self.down = []

    def terminate(self):
        print("ConnectivityEngine going down")
        for k in self.processes.keys():
            self.log.log(s_name, "Terminating: " + k)
            if self.processes[k].is_alive():
                self.processes[k].terminate()
            self.processes[k].join()
        self.log.log(s_name, "Going down...")


def run(exchange, queue):
    exchange.run(queue)
