

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
        self.down = []
        self.lg = log
        pass

    def load_apis(self, cfg_filename, ex_key_filename, wallet_key_filename):
        """Process configuration and api key files"""
        ex_key_d = {}
        wlt_key_d = {}

        #Open and parse config file to get active exchanges and wallets
        f = open(cfg_filename, "r")
        for line in f:
            split_line = line.rstrip('\n').split("=")
            self.cfg_d[split_line[0]] = (split_line[1] == "yes")
        f.close()

        #Get list of actives and write to log
        self.active = [ex for ex in self.cfg_d.keys() if self.cfg_d[ex]]
        out = ""
        for exchange in self.active:
            out += exchange + "\t"
        self.log("Active : " + out)

        #Parse API keys from each exchange
        f = open(ex_key_filename)
        for line in f:
            ex = line.split("_")[0]
            if self.cfg_d[ex]:
                split_line = line.rstrip('\n').split("=")
                ex_key_d[split_line[0]] = \
                    line[len(split_line[0])+1:].rstrip('\n')
        f.close()

        #Parse API keys from each wallet
        f = open(wallet_key_filename)
        for line in f:
            end = line.split("_")[0]
            if self.cfg_d[end]:
                split_line = line.rstrip('\n').split("=")
                wlt_key_d[split_line[0]] = \
                    line[len(split_line[0])+1:].rstrip('\n')
        f.close()

        #Initialize API key objects for all
        for end in self.active:
            self.ex_apis[end] = \
                APIKey(ex_key_d[end + "_key"],
                       ex_key_d[end + "_secret"])
            self.wlt_apis[end] = \
                APIKey(wlt_key_d[end + "_wallet_key"],
                       wlt_key_d[end + "_wallet_secret"])

        self.log("***APIS LOADED***")


    def add_wallets(self):
        """Add wallets"""
        for end in self.active:
            self.wallets[end] = Wallet(ExchangeType.type(end))
        self.log("***WALLETS LOADED***")


    def add_exchanges(self):
        """ Add exchanges"""
        for ex in self.active:
            self.exchanges[ex] = Exchange(ExchangeType.type(ex))
        self.log("***EXCHANGES LOADED***")


    def initialize_exchanges(self):
        for end in self.exchanges.keys():
            self.log(self.wallets[end].APIInit(self.ex_apis[end]))
        self.log("***EXCHANGE APIS INITIALIZED***")


    def initialize_wallets(self):
        """Connect to all endpoints"""
        for end in self.wallets.keys():
            self.log(self.wallets[end].APIInit(self.wlt_apis[end]))
        self.log("***WALLET APIS INITIALIZED***")


    def connect_exchanges(self, recrouter):
        pass

    def connect_wallets(self, recrouter):
        pass


    def heartbeat(self):
        """ """
        self.log("***HEARTBEAT***")
        for end in self.wallets.keys():
            if not wallets[end].heartbeat():
                self.down.append(wallets[end])
        for end in self.exchanges.keys():
            if not exchanges[end].heartbeat():
                self.down.append(exchanges[end])
        return (len(self.down) == 0)


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
        self.initialize_wallets()
        self.connect_wallets()
        self.connect_exchanges()
        self.monitor()

    def monitor(self):
        if self.heartbeat():
            self.log("STATUS: OK")
        else:
            self.log("STATUS: DOWN")
            for down in self.down:
                self.restart(down)

    def restart(self, down):
        '''' '''
        pass

    def close(self):
        self.log("***LOG END***")
        self.lg.close()
