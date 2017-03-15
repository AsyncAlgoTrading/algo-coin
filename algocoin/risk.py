from .lib.config import RiskConfig
from .lib.structs import TradeRequest, TradeResponse, MarketData
from .lib.enums import Side
from .lib.logging import RISK as rlog


class Risk(object):
    def __init__(self, options: RiskConfig) -> None:
        self.max_drawdown = options.max_drawdown
        self.max_risk = options.max_risk
        self.total_funds = options.total_funds
        self.outstanding = 0.0  # type: float

        self.max_running_outstanding = 0.0
        self.max_running_outstanding_incr = []  # type: List

        self.max_running_drawdown = 0.0  # type: float
        self.max_running_drawdown_incr = []  # type: List

        self.max_running_risk = 0.0  # type: float
        self.max_running_risk_incr = []  # type: List

    def _constructResp(self,
                       data: MarketData,
                       side: Side,
                       vol: float,
                       price: float,
                       success: bool,
                       reason: str) -> TradeRequest:
        resp = TradeRequest(data=data, side=side, volume=vol, price=price, risk_check=success, risk_reason=reason)

        if success:
            self.outstanding += abs(vol * price) * (1 if side == Side.BUY else -1)

            self.max_running_outstanding = max(self.max_running_outstanding,
                                               self.outstanding)
            self.max_running_outstanding_incr.append(
                self.max_running_outstanding)

            # TODO self.max_running_risk =
            # TODO self.max_running_drawdown =
        return resp

    def request(self, req: TradeRequest) -> TradeRequest:
        total = req.volume * req.price
        max = self.max_risk/100.0 * self.total_funds

        if (total + self.outstanding) <= max:
            # room for full volume
            rlog.info('Order: %s' % req)
            return self._constructResp(req.data, req.side, req.volume, req.price, True, '')

        elif self.outstanding < max:
            # room for some volume
            volume = (max - self.outstanding) / req.price
            rlog.info('Partial Order: %s' % req)
            return self._constructResp(req.data, req.side, volume, req.price, True, '')

        # no room for volume
        rlog.info('Order rejected: %s' % req)
        return self._constructResp(req.data, req.side, req.volume, req.price, False, 'no room for volume %.2f of %.2f' % (self.outstanding, max))

    def requestBuy(self, req: TradeRequest):
        '''precheck for risk compliance'''
        return self.request(req)

    def requestSell(self, req: TradeRequest):
        '''precheck for risk compliance'''
        return self.request(req)

    def update(self, data: TradeResponse):
        '''update risk after execution'''
        pass
