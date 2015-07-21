

from algo_coin.wallet import *
from algo_coin.exchange import *
from algo_coin.util.util import *

s_name = "CONENG"


class ConnectivityEngine(object):
    def __init__(self, log):
        """ConnectivityEngine needs to build dictionaries of
        api keys based on which wallets and exchanges we
        are going to connect to. Initialize with logfile too"""
        self.cfg_d = {}
        self.active = []
        self.ex_apis = {}
        self.wlt_apis = {}
        self.wallets = {}
        self.exchanges = {}
        self.lg = log
        pass

    def load_apis(self, cfg_filename, ex_key_filename, wallet_key_filename):
        """Process configuration and api key files"""
        ex_key_d = {}
        wlt_key_d = {}

        #Open and parse config file to get active
        #exchanges and wallets
        f = open(cfg_filename, "r")
        for line in f:
            split_line = line.rstrip('\n').split("=")
            self.cfg_d[split_line[0]] = (split_line[1] == "yes")
        f.close()

        #Get list of actives and write to log
        self.active = [exchange for exchange in self.cfg_d.keys()
                       if self.cfg_d[exchange]]
        out = ""
        for exchange in self.active:
            out += exchange + "\t"
        self.log("Active : " + out)

        #Parse API keys from each exchange
        f = open(ex_key_filename)
        for line in f:
            exchange_name = line.split("_")[0]
            if self.cfg_d[exchange_name]:
                split_line = line.rstrip('\n').split("=")
                ex_key_d[split_line[0]] = \
                    line[len(split_line[0])+1:].rstrip('\n')
        f.close()

        #Parse API keys from each wallet
        f = open(wallet_key_filename)
        for line in f:
            exchange_name = line.split("_")[0]
            if self.cfg_d[exchange_name]:
                split_line = line.rstrip('\n').split("=")
                wlt_key_d[split_line[0]] = \
                    line[len(split_line[0])+1:].rstrip('\n')
        f.close()

        #Initialize API key objects for all
        for exchange in self.active:
            self.ex_apis[exchange_name] = \
                APIKey(ex_key_d[exchange_name + "_key"],
                       ex_key_d[exchange_name + "_secret"])
            self.wlt_apis[exchange_name] = \
                APIKey(wlt_key_d[exchange_name + "_wallet_key"],
                       wlt_key_d[exchange_name + "_wallet_secret"])

        self.log("***APIS LOADED***")


    def add_wallets(self):
        """Add wallets"""
        for exchange in self.active:
            self.wallets[exchange] = Wallet(ExchangeType.type(exchange))
        self.log("***WALLETS LOADED***")


    def add_exchanges(self):
        """ Add exchanges"""
        for exchange in self.active:
            self.exchanges[exchange] = Exchange(ExchangeType.type(exchange))
        self.log("***EXCHANGES LOADED***")


    def initialize_endpoints(self):
        #TODO
        pass


    def connect(self):
        """Connect to all endpoints"""
        #TODO
        for exchange in self.active:
            # try:
            #     self.log.log(self.wallets[exchange].APIInit(
            #         self.wlt_apis[exchange]))
            #     self.log.log(self.exchanges[exchange].APIInit(
            #         self.ex_apis[exchange]))
            # except Exception:
            #     print("Initialization failed for: " + exchange)
            self.log(self.wallets[exchange].APIInit(
                self.wlt_apis[exchange]))
            # self.log(self.exchanges[exchange].APIInit(
                # self.ex_apis[exchange]))

        self.log("***APIS INITIALIZED***")

    def heartbeat(self):
        """ """
        #TODO
        self.log("***HEARTBEAT***")
        #TODO for http requests, use specific request
        #TODO for websockets, monitor actual connection
        return False

    def log(self, message):
        """Log a message wrapper"""
        self.lg.log(s_name, message)

    def get_active(self):
        """return list of actively connected exchanges/wallets"""
        return self.active

    def setup(self, config_file, ex_keys_file, wallet_keys_file):
        """Go through full connection stack"""
        self.load_apis(config_file, ex_keys_file, wallet_keys_file)
        self.add_wallets()
        self.add_exchanges()
        self.initialize_endpoints()
        self.connect()

    def monitor(self):
        return self.heartbeat()

    def close(self):
        self.log("***LOG END***")
        self.lg.close()
