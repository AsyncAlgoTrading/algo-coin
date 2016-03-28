

class SendEngine(object):
    def __init__(self, settings, active):
        self.active = active.copy()

    def connect_queues(self, read_queue):
        self.read_queue = read_queue  # from compliance
