from exchange import Exchange
from callback import Print
import time


class TradingEngine(object):
    def __init__(self, sandbox=False, verbose=False):
        self._strats = []
        self._ex = Exchange(sandbox=False)
        if verbose:
            self._ex.registerCallback(
                Print(onMatch=True,
                      onReceived=False,
                      onOpen=False,
                      onDone=False,
                      onChange=False,
                      onError=False))

        self._ticked = []

    def registerStrategy(self, strat):
        self._ex.registerCallback(strat.callback())
        self._strats.append(strat)

    def run(self):
        self._ex.run(self)

    def tick(self):
        for strat in self._strats:
            if strat.ticked():
                self._ticked.append(strat)
                strat.reset()

        self.ticked()

    def ticked(self):
        while len(self._ticked):
            strat = self._ticked.pop()
            print('Strat ticked', strat, time.time())
