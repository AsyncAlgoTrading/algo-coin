
from algo_coin.util.util import *
from algo_coin.apis.coinbase import *


class Exchange(Endpoint):
    def __init__(self, type):
        """ """
        super().__init__(type)

    def APIInit(self, api_key):
        """ """
        if self.type is ExchangeType.coinbase:
            self.exchange_api = CoinbaseExchangeAPI(api_key)

        self.exchange_api.APIInit()

    def buy(self,):
        """ """
        pass

    def sell(self):
        """ """
        pass
