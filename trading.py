from exchange import Exchange
from callback import Print


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

    def registerStrategy(self, strat):
        self._ex.registerCallback(strat.callback())
        self._strats.append(strat)

    def run(self):
        self._ex.run()
