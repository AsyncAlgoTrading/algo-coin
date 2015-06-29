
from enum import Enum, unique


@unique
class WalletType(Enum):
    coinbase = 1
    hitbtc = 2
    cryptsy = 3
    bitfinex = 4
    kraken = 5
    btce = 6


class Wallet(object):
    def __init__(self, type):
        if not isinstance(type, WalletType):
            raise TypeError
        self.type = type

    def get_type(self):
        return self.type
