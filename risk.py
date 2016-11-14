from config import RiskConfig
from structs import MarketData


class Risk(object):
    def __init__(self, options: RiskConfig):
        pass

    def requestBuy(self, data: MarketData):
        pass

    def requestSell(self, data: MarketData):
        pass

    def update(self, data: MarketData):
        pass
