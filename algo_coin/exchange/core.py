
from autobahn.twisted.websocket import WebSocketClientFactory


class AlgoCoinWebSocketClientFactory(WebSocketClientFactory):
    def __init__(self, endpoint, debug=True):
        super().__init__(endpoint, debug)
        pass

    def __repr__(self):
        return str(self.protocol)

    def __str__(self):
        return self.__repr__()


# from algo_coin.endpoint.endpoint import *
# from abc import abstractmethod

# class Exchange(Endpoint):
#     def __init__(self, type):
#         """ """
#         super().__init__(type)

#     @abstractmethod
#     def connect(self):
#         pass

#     @abstractmethod
#     def buy(self,):
#         """ """
#         pass

#     @abstractmethod
#     def sell(self):
#         """ """
#         pass
