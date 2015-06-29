
import algo_coin.dashboard as db
import algo_coin.exchanges as ex
import algo_coin.strategies as st
from algo_coin.wallet import *


class APIKey(object):
    def __init__(self, key, secret_key):
        self.key = key
        self.secret_key = secret_key

    def key(self):
        return self.key

    def secret_key(self):
        return self.secret_key


def test():
    print("test")


def run():
    print("run")


def main():
    w = Wallet(WalletType.coinbase)
    print(w.get_type())
