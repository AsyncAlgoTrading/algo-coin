from config import RiskConfig
from structs import RiskRequest, RiskResponse, ExecutionReport


class Risk(object):
    def __init__(self, options: RiskConfig):
        self.max_drawdown = options.max_drawdown
        self.max_risk = options.max_risk
        self.total_funds = options.total_funds
        self.outstanding = 0.0

        self.max_running_outstanding = 0.0
        self.max_running_outstanding_incr = []

        self.max_running_drawdown = 0.0
        self.max_running_drawdown_incr = []

        self.max_running_risk = 0.0
        self.max_running_risk_incr = []

    def _constructResp(self, side, vol: float, price: float, success: bool) \
            -> RiskResponse:
        resp = RiskResponse()
        resp.side = side
        resp.volume = vol
        resp.price = price
        resp.success = success

        if success:
            # don't care about side for now
            self.outstanding += abs(vol * price)

            self.max_running_outstanding = max(self.max_running_outstanding,
                                               self.outstanding)
            self.max_running_outstanding_incr.append(
                self.max_running_outstanding)

            # TODO self.max_running_risk =
            # TODO self.max_running_drawdown =
        return resp

    def request(self, req: RiskRequest) -> RiskResponse:
        total = req.volume * req.price
        max = self.max_risk/100.0 * self.total_funds
        if (total + self.outstanding) <= max:
            # room for full volume
            return self._constructResp(req.side, req.volume, req.price, True)

        elif self.outstanding < max:
            # room for some volume
            volume = (max - self.outstanding) / req.price
            return self._constructResp(req.side, volume, req.price, True)

        # no room for volume
        return self._constructResp(req.side, req.volume, req.price, False)

    def requestBuy(self, req: RiskRequest) -> RiskResponse:
        return self.request(req)

    def requestSell(self, req: RiskRequest) -> RiskResponse:
        return self.request(req)

    def update(self, data: ExecutionReport):
        pass
