from config import ExecutionConfig
from exchange import Exchange
from structs import TradeRequest, TradeResponse


class Execution(object):
    def __init__(self, options: ExecutionConfig, exchange: Exchange):
        pass

    def requestBuy(self, req: TradeRequest) -> TradeResponse:
        pass

    def requestSell(self, req: TradeRequest) -> TradeResponse:
        pass
