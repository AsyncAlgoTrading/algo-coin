
import time
from datetime import datetime

from algo_coin.wallet import *
from algo_coin.exchange import *
from algo_coin.util import *


class AlgoCoin(object):
    def __init__(self):
        """ """
        self.cfg_d = {}
        self.active = []
        self.ex_key_d = {}
        self.wlt_key_d = {}
        self.ex_apis = {}
        self.wlt_apis = {}
        self.wallets = {}
        self.exchanges = {}

        self.logfile = open("logs/log-" + str(int(time.time())), "w")
        self.log("***LOG START***")
        pass

    def log(self, string):
        """ """
        self.logfile.write(str(datetime.now()) + "\t" + string + "\n")

    def load_apis(self, cfg_filename, ex_key_filename, wallet_key_filename):
        """ """
        #
        #
        #
        f = open(cfg_filename, "r")
        for line in f:
            split_line = line.rstrip('\n').split("=")
            self.cfg_d[split_line[0]] = (split_line[1] == "yes")
        f.close()

        #comments
        #
        #
        self.active = [exchange for exchange in self.cfg_d.keys()
                       if self.cfg_d[exchange]]
        out = ""
        for exchange in self.active:
            out += exchange + "\t"
            self.log("Active : " + out)

        #
        #
        #
        f = open(ex_key_filename)
        for line in f:
            exchange_name = line.split("_")[0]
            if self.cfg_d[exchange_name]:
                split_line = line.rstrip('\n').split("=")
                self.ex_key_d[split_line[0]] = \
                    line[len(split_line[0])+1:].rstrip('\n')
        f.close()

        #
        #
        #
        f = open(wallet_key_filename)
        for line in f:
            exchange_name = line.split("_")[0]
            if self.cfg_d[exchange_name]:
                split_line = line.rstrip('\n').split("=")
                self.wlt_key_d[split_line[0]] = \
                    line[len(split_line[0])+1:].rstrip('\n')
        f.close()

        #
        #
        #
        for exchange in self.active:
            self.ex_apis[exchange_name] = APIKey(self.ex_key_d[exchange_name + "_key"], self.ex_key_d[exchange_name + "_secret"])
            self.wlt_apis[exchange_name] = APIKey(self.wlt_key_d[exchange_name + "_wallet_key"], self.wlt_key_d[exchange_name + "_wallet_secret"])

        self.log("***APIS LOADED***")

        #deallocate
        self.ex_key_d = None
        self.wlt_key_d = None

    def add_wallets(self):
        """ """
        for exchange in self.active:
            self.wallets[exchange] = Wallet(ExchangeType.type(exchange))
        self.log("***WALLETS LOADED***")

    def add_exchanges(self):
        """ """
        for exchange in self.active:
            self.exchanges[exchange] = Exchange(ExchangeType.type(exchange))
        self.log("***EXCHANGES LOADED***")

    def initialize_apis(self):
        """ """
        for exchange in self.active:
            self.wallets[exchange].APIInit(self.wlt_apis[exchange])
            self.exchanges[exchange].APIInit(self.ex_apis[exchange])
        self.log("***APIS INITIALIZED***")

    def heartbeat(self):
        """ """
        self.log("***HEARTBEAT***")
        pass

    def main(self, config_file, ex_keys_file, wallet_keys_file):
        """ """
        self.load_apis(config_file, ex_keys_file, wallet_keys_file)
        self.add_wallets()
        self.add_exchanges()
        self.initialize_apis()
        self.heartbeat()
        self.log("***LOG END***")
        self.logfile.close()
