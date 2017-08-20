from .lib.config import ExecutionConfig
from .lib.exchange import Exchange
from .lib.enums import Side, CurrencyType
from .lib.structs import TradeRequest, TradeResponse, MarketData
from .lib.logging import EXEC as exlog


class Execution(object):
    def __init__(self, options: ExecutionConfig, exchange: Exchange) -> None:
        self._ex = exchange
        self._exs = []

    def requestBuy(self, req: TradeRequest) -> TradeResponse:
        resp = self._ex.buy(req)
        exlog.info('Order executed: %s' % resp)
        return resp

    def requestSell(self, req: TradeRequest) -> TradeResponse:
        resp = self._ex.sell(req)
        exlog.info('Order executed: %s' % resp)
        return resp

    def request(self, req: TradeRequest) -> TradeResponse:
        if req.side == Side.BUY:
            return self.requestBuy(req)
        return self.requestSell(req)
