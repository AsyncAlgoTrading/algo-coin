from exchange import Exchange
from callback import Print
from backtest import Backtest
from options import TradingEngineConfig
from enums import TradingType
# import time


class TradingEngine(object):
    def __init__(self, options: TradingEngineConfig):
        self._live = options.type == TradingType.LIVE
        self._sandbox = options.type == TradingType.SANDBOX
        self._backtest = options.type == TradingType.BACKTEST
        self._verbose = options.verbose

        self._strats = []
        self._ex = Exchange(options.exchange_options)
        self._bt = Backtest(options.backtest_options)

        if self._verbose:
            print('WARNING: Running in verbose mode')

            self._ex.registerCallback(
                Print(onMatch=True,
                      onReceived=False,
                      onOpen=False,
                      onDone=False,
                      onChange=False,
                      onError=False))
            self._bt.registerCallback(Print())

        self._ticked = []

    def registerStrategy(self, strat):
        if self._live or self._sandbox:
            # register for exchange data
            self._ex.registerCallback(strat.callback())

        if self._backtest:
            # register for backtest data
            self._bt.registerCallback(strat.callback())

        # add to tickables
        self._strats.append(strat)  # add to tickables

        # give self to strat so it can request trading actions
        strat._te = self

    def run(self):
        if self._live or self._sandbox:
            self._ex.run(self)
        elif self._backtest:
            self._bt.run(self)
        else:
            raise Exception('Invalid configuration')

    def tick(self):
        for strat in self._strats:
            if strat.ticked():
                self._ticked.append(strat)
                strat.reset()

        self.ticked()

    def ticked(self):
        while len(self._ticked):
            self._ticked.pop()
            # strat = self._ticked.pop()
            # print('Strat ticked', strat, time.time())
