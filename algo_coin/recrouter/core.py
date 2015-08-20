
from multiprocessing import Queue
import algo_coin.exchange as ex


class ReceiverRouter(object):
    def __init__(self, settings, active, endpoints):
        self.active = active.copy()
        self.endpoints = endpoints.copy()
        self.websockets = {}
        self.threads = [self.setup(end) for end in self.active]
        print(self.threads)

    def setup_thread_queues(self):
        self.thread_queues = [Queue() for thread in self.active]

    def get_thread_queues(self):
        return self.thread_queues

    def connect_queues(self, write_queue, comp_queue):
        self.write_queue = write_queue  # to stratman
        self.compliance = comp_queue  # to compliance

    def setup(self, endpoint):
        f = ex.AlgoCoinWebSocketClientFactory(self.endpoints[endpoint],
                                              debug=True)
        f.protocol = load_protocol(endpoint)
        return f


def load_protocol(endpoint):
    if endpoint == "coinbase":
        return ex.CoinbaseExchangeClientProtocol
    pass
