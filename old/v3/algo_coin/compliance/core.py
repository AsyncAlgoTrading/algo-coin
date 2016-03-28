

class Compliance(object):
    def __init__(self, settings, active):
        self.active = active.copy()

    def connect_queues(self, receiver_queue, strategy_queue, sendeng_queue):
        self.receiver_queue = receiver_queue  # from recrouter
        self.strategy_queue = strategy_queue  # from stratman
        self.sendeng_queue = sendeng_queue
