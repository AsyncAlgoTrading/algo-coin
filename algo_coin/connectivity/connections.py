
from algo_coin.util.api import APIKey
from algo_coin.exchange.coinbase_exchange import CoinbaseExchangeClient
from algo_coin.endpoint.endpoint import EndpointType
import time

s_name = "Connections"


class Connections(object):
    def __init__(self, config_file, ex_keys, log):
        self.log = log
        self.active = []
        self.exchanges = {}
        self.load(config_file, ex_keys)

    def load(self, cfg_filename, ex_key_filename):
        self.log.log(s_name, "Loading Configurations")
        cfg_d = {}
        ex_key_d = {}
        ex_apis = {}

        f = open(cfg_filename, "r")
        for line in f:
            split_line = line.rstrip('\n').split("=")
            cfg_d[split_line[0]] = (split_line[1] == "yes")
        f.close()

        self.active = [ex for ex in cfg_d.keys() if cfg_d[ex]]
        out = ""
        for exchange in self.active:
            out += exchange + "\t"
        # self.log("Active : " + out)

        f = open(ex_key_filename)
        for line in f:
            ex = line.split("_")[0]
            if cfg_d[ex]:
                split_line = line.rstrip('\n').split("=")
                ex_key_d[split_line[0]] = \
                    line[len(split_line[0])+1:].rstrip('\n')
        f.close()

        for end in self.active:
            ex_apis[end] = \
                APIKey(ex_key_d[end + "_key"],
                       ex_key_d[end + "_secret"])

        for ex in self.active:
            self.exchanges[ex] = LoadExchange(EndpointType.type(ex), "")  # TODO

        self.log.log(s_name, "Configurations loaded")

    def get_active(self):
        return self.active

    def get_exchanges(self):
        return self.exchanges


def LoadExchange(endpoint_type, endpoint):
    if(endpoint_type is EndpointType.coinbase):
        return CoinbaseExchangeClient(
            endpoint, open("logs/log-Coinbase-" +
                           str(int(time.time())), "w"))
