
from multiprocessing import Queue


class ReceiverRouter(object):
    def __init__(self, settings, active, endpoints):
        self.active = active.copy()
        self.endpoints = endpoints.copy()
        self.threads = [setup(end) for end in self.active]
        print(self.threads)

    def setup_thread_queues(self):
        self.thread_queues = [Queue() for thread in self.active]

    def get_thread_queues(self):
        return self.thread_queues

    def connect_queues(self, write_queue, comp_queue):
        self.write_queue = write_queue  # to stratman
        self.compliance = comp_queue  # to compliance


def setup(endpoint):
    if endpoint == "coinbase":
        return 1
    return 0
