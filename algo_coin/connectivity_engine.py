
from algo_coin.wallet import *
from algo_coin.exchange import *
from algo_coin.util import *


class ConnectivityEngine(object):
    def __init__(self, log):
        """ """
        self.cfg_d = {}
        self.active = []
        self.ex_apis = {}
        self.wlt_apis = {}
        self.wallets = {}
        self.exchanges = {}
        self.log = log
        pass

    def load_apis(self, cfg_filename, ex_key_filename, wallet_key_filename):
        """ """
        ex_key_d = {}
        wlt_key_d = {}
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
            self.log.log("Active : " + out)

        #
        #
        #
        f = open(ex_key_filename)
        for line in f:
            exchange_name = line.split("_")[0]
            if self.cfg_d[exchange_name]:
                split_line = line.rstrip('\n').split("=")
                ex_key_d[split_line[0]] = \
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
                wlt_key_d[split_line[0]] = \
                    line[len(split_line[0])+1:].rstrip('\n')
        f.close()

        #
        #
        #
        for exchange in self.active:
            self.ex_apis[exchange_name] = \
                APIKey(ex_key_d[exchange_name + "_key"],
                       ex_key_d[exchange_name + "_secret"])
            self.wlt_apis[exchange_name] = \
                APIKey(wlt_key_d[exchange_name + "_wallet_key"],
                       wlt_key_d[exchange_name + "_wallet_secret"])

        self.log.log("***APIS LOADED***")

    def add_wallets(self):
        """ """
        for exchange in self.active:
            self.wallets[exchange] = Wallet(ExchangeType.type(exchange))
        self.log.log("***WALLETS LOADED***")

    def add_exchanges(self):
        """ """
        for exchange in self.active:
            self.exchanges[exchange] = Exchange(ExchangeType.type(exchange))
        self.log.log("***EXCHANGES LOADED***")

    def initialize_apis(self):
        """ """
        for exchange in self.active:
            # try:
            #     self.log.log(self.wallets[exchange].APIInit(
            #         self.wlt_apis[exchange]))
            #     self.log.log(self.exchanges[exchange].APIInit(
            #         self.ex_apis[exchange]))
            # except Exception:
            #     print("Initialization failed for: " + exchange)
            self.log.log(self.wallets[exchange].APIInit(
                self.wlt_apis[exchange]))
            # self.log.log(self.exchanges[exchange].APIInit(
                # self.ex_apis[exchange]))

        self.log.log("***APIS INITIALIZED***")

    def heartbeat(self):
        """ """
        self.log.log("***HEARTBEAT***")
        pass

    def setup(self, config_file, ex_keys_file, wallet_keys_file):
        """ """
        self.load_apis(config_file, ex_keys_file, wallet_keys_file)
        self.add_wallets()
        self.add_exchanges()
        self.initialize_apis()
        self.heartbeat()
        self.log.log("***LOG END***")
        self.log.close()
