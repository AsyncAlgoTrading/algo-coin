
from algo_coin.util import *
from algo_coin.apis.core import *

from coinbase.client import Client


class CoinbaseWalletAPI(WalletAPI):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Coinbase-Wallet"

    def APIInit(self):
        self.client = Client(self.api_key.get_key(),
                             self.api_key.get_secret_key())
        print(self.client.get_accounts())
        return("Connected: " + self.name)

    def deposit(self, source):
        pass

    def withdraw(self, destination):
        pass


class CoinbaseExchangeAPI(WalletAPI):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Coinbase-Exchange"

    def APIInit(self):
        self.client = Client(self.api_key.get_key(),
                             self.api_key.get_secret_key())
        print(self.client.get_accounts())
        return("Connected: " + self.name)

    def deposit(self, source):
        pass

    def withdraw(self, destination):
        pass
