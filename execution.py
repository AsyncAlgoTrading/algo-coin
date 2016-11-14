from config import ExecutionConfig
from exchange import Exchange
from structs import TradeRequest, TradeResponse


class Execution(object):
    def __init__(self, options: ExecutionConfig, exchange: Exchange):
        pass

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
        return self._constructResponse(req.side, req.volume, req.price, True)

    def requestSell(self, req: TradeRequest) -> TradeResponse:
        # TODO
        return self._constructResponse(req.side, req.volume, req.price, True)
