from config import ExecutionConfig
from exchange import Exchange
from structs import MarketData


class Execution(object):
    def __init__(self, options: ExecutionConfig, exchange: Exchange):
        pass

    def requestBuy(self, data: MarketData):
        pass

    def requestSell(self, data: MarketData):
        pass
