from config import RiskConfig
from structs import TradeRequest, TradeResponse, ExecutionReport


class Risk(object):
    def __init__(self, options: RiskConfig):
        self.max_drawdown = options.max_drawdown
        self.max_risk = options.max_risk
        self.total_funds = options.total_funds
        self.outstanding = 0.0

    def _constructResp(self, side, vol: float, price: float, success: bool):
        resp = TradeResponse()
        resp.side = side
        resp.volume = vol
        resp.price = price
        resp.success = success

        # don't care about side for now
        self.outstanding += abs(self.volume * self.price)

        return resp

    def request(self, req: TradeRequest):
        total = req.volume * req.price
        max = self.max_risk * self.total_funds

        if total + self.outstanding < max:
            # room for full volume
            return self._constructResp(req.side, req.volume, req.price, True)

        elif self.outstanding < max:
            # room for some volume
            volume = (max - self.outstanding) / req.price
            return self._constructResp(req.side, volume, req.price, True)

        # no room for volume
        return self._constructResp(req.side, req.volume, req.price, False)

    def requestBuy(self, req: TradeRequest):
        return self.request(req)

    def requestSell(self, req: TradeRequest):
        return self.request(req)

    def update(self, data: ExecutionReport):
        pass
