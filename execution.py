from config import ExecutionConfig
from exchange import Exchange
from enums import Side
from structs import TradeRequest, TradeResponse


class Execution(object):
    def __init__(self, options: ExecutionConfig, exchange: Exchange):
        self._ex = exchange

    def _constructResp(self, side, vol: float, price: float, success: bool) \
            -> TradeResponse:
        resp = TradeResponse()
        resp.side = side
        resp.volume = vol
        resp.price = price
        resp.success = success
        return resp

    def requestBuy(self, req: TradeRequest) -> TradeResponse:
        # TODO
        # res = self._ex.buy(req)
        return self._constructResp(req.side, req.volume, req.price, True)

    def requestSell(self, req: TradeRequest) -> TradeResponse:
        # TODO
        return self._constructResp(req.side, req.volume, req.price, True)

    def request(self, req: TradeRequest) -> TradeResponse:
        if req.side == Side.BUY:
            return self.requestBuy(req)
        return self.requestSell(req)
