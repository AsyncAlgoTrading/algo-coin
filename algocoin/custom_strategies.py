from .lib.strategy import ticks, \
                          TradingStrategy, \
                          BacktestTradingStrategy
from .lib.structs import MarketData
from .lib.logging import STRAT as slog, ERROR as elog


class SMACrosses(object):
    def initialize(self, size_short, size_long):
        self.short = size_short
        self.shorts = []
        self.short_av = 0.0

        self.long = size_long
        self.longs = []
        self.long_av = 0.0

        self.prev_state = ''
        self.state = ''

        self.bought = 0.0
        self.profits = 0.0

        self._intitialvalue = None
        self._portfolio_value = []

    def onBuy(self, data: MarketData):
        if self._intitialvalue is None:
            date = data.time
            self._intitialvalue = (date, data.price)
            self._portfolio_value.append(self._intitialvalue)

        self.bought = data.price
        slog.info('d->g:bought at %d' % self.bought)

    def onSell(self, data: MarketData):
        profit = data.price - self.bought
        self.profits += profit
        slog.info('g->d:sold at %d - %d - %d' % (data.price, profit, self.profits))
        self.bought = 0.0

        date = data.time
        self._portfolio_value.append((
                date,
                self._portfolio_value[-1][1] + profit))

    @ticks
    def onMatch(self, data: MarketData):
        # add data to arrays
        self.shorts.append(data.price)
        self.longs.append(data.price)

        # check requirements
        if len(self.shorts) > self.short:
            self.shorts.pop(0)

        if len(self.longs) > self.long:
            self.longs.pop(0)

        # calc averages
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

    def onError(self, e):
        elog.critical(e)

    def onAnalyze(self, _):
        import pandas
        import matplotlib.pyplot as plt
        import seaborn as sns
        # pd = pandas.DataFrame(self._actions,
        #                       columns=['time', 'action', 'price'])
        pd = pandas.DataFrame(self._portfolio_value, columns=['time', 'value'])
        pd.set_index(['time'], inplace=True)
        # log.info(pd)

        # sp500 = pandas.DataFrame()
        # tmp = pandas.read_csv('./data/sp/sp500_v_kraken.csv')
        # sp500['Date'] = pandas.to_datetime(tmp['Date'])
        # sp500['Close'] = tmp['Close']
        # sp500.set_index(['Date'], inplace=True)
        # print(sp500)

        sns.set_style('darkgrid')
        fig, ax1 = plt.subplots()

        plt.title('BTC mean-rev algo 1 performance')
        ax1.plot(pd)

        ax1.set_ylabel('Portfolio value($)')
        ax1.set_xlabel('Date')
        for xy in [self._portfolio_value[0]] + [self._portfolio_value[-1]]:
            ax1.annotate('$%s' % xy[1], xy=xy, textcoords='data')

        # ax2 = ax1.twinx()
        # ax2.plot(sp500, 'r')
        # ax2.set_ylabel('S&P500 ($)')
        plt.show()

    def slippage(self, data):
        slog.critical(data)
        return data

    def transactionCost(self, data):
        slog.critical(data)
        return data


class SMACrossesStrategy(TradingStrategy):
    def __init__(self, size_short: int, size_long: int):
        super(SMACrossesStrategy, self).__init__()
        # TODO autobind?
        self.initialize = SMACrosses.initialize.__get__(self)
        self.onBuy = SMACrosses.onBuy.__get__(self)
        self.onSell = SMACrosses.onSell.__get__(self)
        self.onMatch = SMACrosses.onMatch.__get__(self)
        self.onError = SMACrosses.onError.__get__(self)
        self.onAnalyze = SMACrosses.onAnalyze.__get__(self)
        self.initialize(size_short, size_long)


class SMACrossesBacktest(BacktestTradingStrategy):
    def __init__(self, size_short: int, size_long: int):
        super(SMACrossesBacktest, self).__init__()
        # TODO autobind?
        self.initialize = SMACrosses.initialize.__get__(self)
        self.onBuy = SMACrosses.onBuy.__get__(self)
        self.onSell = SMACrosses.onSell.__get__(self)
        self.onMatch = SMACrosses.onMatch.__get__(self)
        self.onError = SMACrosses.onError.__get__(self)
        self.onAnalyze = SMACrosses.onAnalyze.__get__(self)
        self.slippage = SMACrosses.slippage.__get__(self)
        self.transactionCost = SMACrosses.transactionCost.__get__(self)
        self.initialize(size_short, size_long)
