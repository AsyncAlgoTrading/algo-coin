
from multiprocessing import Queue


class StrategyManager(object):
    def __init__(self, settings, active):
        self.active = active.copy()
        self.threads = [setup(end) for end in self.active]

    def setup_thread_queues(self):
        self.thread_queues = [Queue() for thread in self.active]
        pass

    def get_thread_queues(self):
        return self.thread_queues

    def connect_queues(self, read_queue, comp_queue):
        self.read_queue = read_queue  # from recrouter
        self.compliance = comp_queue  # to compliance


def setup(endpoint):
    if endpoint == "coinbase":
        return 1
    return 0
