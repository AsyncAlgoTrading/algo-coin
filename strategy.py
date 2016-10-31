from callback import Callback, NullCallback
from abc import ABCMeta, abstractmethod


class Strategy(metaclass=ABCMeta):
    '''Strategy interface'''

    @abstractmethod
    def ticked(self):
        '''strategy has ticked'''


class TradingStrategy(Strategy, Callback):
    def callback(self):
        return self


class NullTradingStrategy(Strategy, NullCallback):
    def callback(self):
        return self


class SMACrossesStrategy(NullTradingStrategy):
    def __init__(self, size_short, size_long):
        super(SMACrossesStrategy, self).__init__()

        self.short = size_short
        self.shorts = []
        self.short_av = 0

        self.long = size_long
        self.longs = []
        self.long_av = []

        self.prev_state = ''
        self.state = ''

    def onMatch(self, data):
        self.shorts.append(float(data['price']))
        self.longs.append(float(data['price']))

        if len(self.shorts) > self.short:
            self.shorts.pop(0)

        if len(self.longs) > self.long:
            self.longs.pop(0)

        self.short_av = float(sum(self.shorts)) / max(len(self.shorts), 1)
        self.long_av = float(sum(self.longs)) / max(len(self.longs), 1)

        self.prev_state = self.state
        if self.short_av > self.long_av:
            self.state = 'golden'
        elif self.short_av < self.long_av:
            self.state = 'death'
        else:
            self.state = ''

    def ticked(self):
        if len(self.longs) < self.long:
            return
        print("short_av", self.short_av, len(self.shorts))
        print("long_av", self.long_av, len(self.longs))
        if self.state == 'golden' and self.prev_state != 'golden':
            print('BUY!')
        elif self.state == 'death' and self.prev_state != 'death':
            print('SELL!')
