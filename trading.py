from exchange import Exchange
from callback import Print
from backtest import BackTest
# import time


class TradingEngine(object):
    def __init__(self,
                 live=True,        # Run with exchange
                 sandbox=False,    # Run with sandbox
                 backtest=False,   # Run with backtest
                 verbose=False,    # Debug print
                 *args,
                 **kwargs):

        self._live = live
        self._sandbox = sandbox
        self._backtest = backtest
        self._verbose = verbose

        self._strats = []
        self._ex = Exchange(sandbox=sandbox)
        self._bt = BackTest(kwargs.get('bt_file', ''))

        if verbose:
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
