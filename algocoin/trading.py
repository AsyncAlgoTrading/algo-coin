from typing import Callable
from .backtest import Backtest
from .lib.callback import Callback, Print
from .lib.config import TradingEngineConfig
from .lib.enums import TradingType, Side, CurrencyType
from .execution import Execution
from .risk import Risk
from .lib.strategy import TradingStrategy
from .lib.structs import TradeRequest, TradeResponse
from .lib.utils import ex_type_to_ex
from .lib.logging import LOG as log, SLIP as sllog, TXNS as tlog
# import time


class TradingEngine(object):
    def __init__(self, options: TradingEngineConfig) -> None:
        self._live = options.type == TradingType.LIVE
        self._sandbox = options.type == TradingType.SANDBOX
        self._backtest = options.type == TradingType.BACKTEST
        self._print = options.print

        self._strats = []  # type: List[TradingStrategy]

        self._ex = ex_type_to_ex(options.exchange_options.exchange_type)(options.exchange_options) if self._live or self._sandbox else None

        if self._live or self._sandbox:
            accounts = self._ex.accounts()

            # extract max funds info
            for account in accounts:
                if account.currency == CurrencyType.USD:
                    options.risk_options.total_funds = account.balance

            log.info(accounts)
            log.info("Running with %.2f USD" % options.risk_options.total_funds)


        self._bt = Backtest(options.backtest_options) if self._backtest else None
        self._rk = Risk(options.risk_options)
        self._ec = Execution(options.execution_options, self._ex)

        # sanity check
        assert not (self._live and self._sandbox and self._backtest)

        if self._print:
            log.warn('WARNING: Running in verbose mode')

            if self._live or self._sandbox:
                self._ex.registerCallback(
                    Print(onTrade=True,
                          onReceived=False,
                          onOpen=False,
                          onDone=False,
                          onChange=False,
                          onError=False))

            if self._backtest:
                self._bt.registerCallback(Print())

        self._ticked = []  # type: List
        self._trading = True  # type: bool

    def exchange(self):
        return self._ex

    def backtest(self):
        return self._bt

    def risk(self):
        return self._rk

    def execution(self):
        return self._ec

    def haltTrading(self):
        self._trading = False

    def continueTrading(self):
        self._trading = True

    def registerStrategy(self, strat: TradingStrategy):
        if self._live or self._sandbox:
            # register for exchange data
            self._ex.registerCallback(strat.callback())

        elif self._backtest:
            # register for backtest data
            self._bt.registerCallback(strat.callback())

        # add to tickables
        self._strats.append(strat)  # add to tickables

        # give self to strat so it can request trading actions
        strat.setEngine(self)

    def run(self):
        if self._live or self._sandbox:
            # run on exchange
            self._ex.run(self)

        elif self._backtest:
            # let backtester run
            self._bt.run(self)

        else:
            raise Exception('Invalid configuration')

    def tick(self):
        for strat in self._strats:
            # only if strat ticked
            if strat.ticked():
                self._ticked.append(strat)
                strat.reset()
        self.ticked()

    def ticked(self):
        while len(self._ticked):
            self._ticked.pop()
            # strat = self._ticked.pop()
            # print('Strat ticked', strat, time.time())

    def _request(self,
                 side: Side,
                 callback: Callable,
                 req: TradeRequest,
                 callback_failure=None,
                 strat=None):
        if not self._trading:
            # not allowed to trade right now
            resp = TradeResponse(data=req.data,
                                 request=req,
                                 side=req.side,
                                 volume=0.0,
                                 price=0.0,
                                 currency=req.currency,
                                 success=False)

        else:
            # get risk report
            resp = self._rk.request(req)

            if resp.risk_check:
                # if risk passes, let execution execute
                resp = self._ec.request(resp)

                sllog.info("Slippage - %s" % resp)
                tlog.info("TXN cost - %s" % resp)
                # let risk update according to execution details
                self._rk.update(resp)
            else:
                resp = TradeResponse(data=resp.data,
                                     request=resp,
                                     side=resp.side,
                                     volume=0.0,
                                     price=0.0,
                                     currency=req.currency,
                                     success=False)

        if self._backtest and strat:
            print("HERE")
            # register the initial request
            strat.registerDesire(req.data.time, req.side, req.price)

            # adjust response with slippage and transaction cost modeling
            resp = strat.slippage(resp)
            sllog.info("Slippage BT- %s" % resp)

            resp = strat.transactionCost(resp)
            tlog.info("TXN cost BT- %s" % resp)

            # register the response
            strat.registerAction(resp.data.time, resp.side, resp.price)

        callback_failure(resp) if callback_failure and not resp.success else callback(resp)

    def requestBuy(self,
                   callback: Callable,
                   req: TradeRequest,
                   callback_failure=None,
                   strat=None):
        self._request(Side.BUY, callback, req, callback_failure, strat)

    def requestSell(self,
                    callback: Callable,
                    req: TradeRequest,
                    callback_failure=None,
                    strat=None):
        self._request(Side.SELL, callback, req, callback_failure, strat)
