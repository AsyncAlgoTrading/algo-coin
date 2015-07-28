
class ReceiverRouter(object):
    def __init__(self, conn_engine):
        self.queues = conn_engine.queues
