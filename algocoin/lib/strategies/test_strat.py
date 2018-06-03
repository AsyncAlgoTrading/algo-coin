from ..strategy import TradingStrategy
from ..structs import MarketData, TradeRequest, TradeResponse
from ..enums import Side, TradeResult, OrderType
from ..logging import STRAT as slog, ERROR as elog


class TestStrategy(TradingStrategy):
    def __init__(self) -> None:
        super(TestStrategy, self).__init__()
        self.active = False
        self.prev_state = ''
        self.state = ''

        self.bought = 0.0
        self.bought_qty = 0.0
        self.profits = 0.0

    def onBuy(self, res: TradeResponse) -> None:
        if res.status not in (TradeResult.FILLED, TradeResult.PARTIAL):
            slog.critical('order failure: %s' % res)
            return

        if res.status == TradeResult.PARTIAL:
            slog.critical('waiting to buy: %.2f @ %.2f' % (res.request.volume, res.request.price))

        else:
            self.active = True
            self.bought = res.volume*res.price
            self.bought_qty = res.volume
            slog.critical('bought: %.2f @ %.2f for %.2f' % (res.volume, res.price, self.bought))

    def onSell(self, res: TradeResponse) -> None:
        if res.status not in (TradeResult.FILLED, TradeResult.PARTIAL):
            slog.info('order failure: %s' % res)
            return

        if res.status == TradeResult.PARTIAL:
            slog.critical('waiting to sell: %.2f @ %.2f' % (res.request.volume, res.request.price))

        else:
            self.active = False
            sold = res.volume*res.price
            profit = sold - self.bought
            self.profits += profit
            slog.critical('sold: %.2f @ %.2f for %.2f - %.2f - %.2f' % (res.volume, res.price, sold, profit, self.profits))
            self.bought = 0.0
            self.bought_qty = 0.0

    def onTrade(self, data: MarketData) -> bool:
        if not self.active:
            req = TradeRequest(side=Side.BUY,
                               volume=1.0,
                               currency=data.currency,
                               order_type=OrderType.MARKET,
                               price=data.price)
            slog.critical("requesting buy : %s", req)
            self.requestBuy(self.onBuy, req)
            self.active = True
            return True
        else:
            if self.bought_qty:
                req = TradeRequest(side=Side.SELL,
                                   volume=self.bought_qty,
                                   currency=data.currency,
                                   order_type=OrderType.MARKET,
                                   price=data.price)
                slog.critical("requesting sell : %s", req)
                self.requestSell(self.onSell, req)
                self.active = False
                return True
            else:
                slog.critical('None bought yet!')
        return False

    def onError(self, e) -> None:
        elog.critical(e, type(e))

    def onExit(self) -> None:
        self.cancelAll(lambda *args: True)

    def onChange(self, data: MarketData) -> None:
        slog.critical(data)

    def onDone(self, data: MarketData) -> None:
        slog.critical(data)

    def onOpen(self, data: MarketData) -> None:
        slog.critical(data)

    def onReceived(self, data: MarketData) -> None:
        slog.critical(data)

    def slippage(self, resp: TradeResponse) -> TradeResponse:
        return resp

    def transactionCost(self, resp: TradeResponse) -> TradeResponse:
        return resp
