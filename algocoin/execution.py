from .lib.config import ExecutionConfig
from .lib.exchange import Exchange
from .lib.enums import Side, CurrencyType
from .lib.structs import TradeRequest, TradeResponse, MarketData
from .lib.logging import EXEC as exlog


class Execution(object):
    def __init__(self, options: ExecutionConfig, exchange: Exchange) -> None:
        self._ex = exchange

    def _constructResp(self,
                       data: MarketData,
                       request: TradeRequest,
                       side: Side,
                       vol: float,
                       price: float,
                       currency: CurrencyType,
                       success: bool)-> TradeResponse:
        resp = TradeResponse(data=data,
                             request=request,
                             side=side,
                             volume=vol,
                             price=price,
                             currency=currency,
                             success=success)
        return resp

    def requestBuy(self, req: TradeRequest) -> TradeResponse:
        # TODO
        # res = self._ex.buy(req)
        resp = self._constructResp(req.data, req, req.side, req.volume, req.price, req.currency, True)
        exlog.info('Order executed: %s' % resp)
        return resp

    def requestSell(self, req: TradeRequest) -> TradeResponse:
        # TODO
        resp = self._constructResp(req.data, req, req.side, req.volume, req.price, req.currency, True)
        exlog.info('Order executed: %s' % resp)
        return resp

    def request(self, req: TradeRequest) -> TradeResponse:
        if req.side == Side.BUY:
            return self.requestBuy(req)
        return self.requestSell(req)
