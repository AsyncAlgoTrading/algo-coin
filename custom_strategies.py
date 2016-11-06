from strategy import ticks, NullTradingStrategy


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

        self.bought = 0.0
        self.profits = 0.0

    def onBuy(self, data):
        self.bought = float(data['price'])
        print('death->golden:bought: ', self.bought)

    def onSell(self, data):
        profit = float(data['price']) - self.bought
        self.profits += profit
        print('golden->death:profit: ', profit, self.profits)
        self.bought = 0.0

    @ticks
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

        if len(self.longs) < self.long or len(self.shorts) < self.short:
            return False

        if self.state == 'golden' and self.prev_state != 'golden' and \
                self.bought == 0.0:  # watch for floating point error
            self.requestBuy(self.onBuy, data)
            return True

        elif self.state == 'death' and self.prev_state != 'death' and \
                self.bought > 0.0:
            self.requestSell(self.onSell, data)
            return True

        return False
