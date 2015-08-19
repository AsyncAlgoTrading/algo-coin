

class ReceiverRouter(object):
    def __init__(self, settings, active, endpoints):
        try:
            self.active = active.copy()
            self.endpoints = endpoints.copy()

        except KeyError:
            raise KeyError
