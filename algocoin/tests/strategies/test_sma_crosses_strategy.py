from mock import patch, MagicMock


class TestSMACrossesStrategy:
    def setup(self):
        pass
        # setup() before each test method

    def teardown(self):
        pass
        # teardown() after each test method

    @classmethod
    def setup_class(cls):
        pass
        # setup_class() before any methods in this class

    @classmethod
    def teardown_class(cls):
        pass
        # teardown_class() after any methods in this class

    def test_sma_strat_init(self):
        from ...lib.strategies.sma_crosses_strategy import SMACrossesStrategy
        s = SMACrossesStrategy(1, 5)
        assert s

    def test_sma_match(self):
        from ...lib.strategies.sma_crosses_strategy import SMACrossesStrategy
        from ...lib.enums import TickType, Side
        from ...lib.structs import MarketData
        from ...lib.utils import parse_date

        s = SMACrossesStrategy(1, 5)
        s._te = MagicMock()

        data = [MarketData(type=TickType.TRADE,
                           time=parse_date('1479272400'),
                           price=float(x),
                           volume=float(100),
                           side=Side.BUY) for x in range(10)]

        for x in range(10):
            s.onTrade(data[x])

        assert s.shorts == [9]
        assert s.longs == [5, 6, 7, 8, 9]

        assert s.short_av == 9
        assert s.long_av == 7

    def test_sma_buy(self):
        from ...lib.strategies.sma_crosses_strategy import SMACrossesStrategy
        from ...lib.enums import TickType, Side
        from ...lib.structs import MarketData, TradeResponse
        from ...lib.utils import parse_date

        s = SMACrossesStrategy(1, 5)

        s._te = MagicMock()
        s._te.requestBuy = MagicMock()
        s._te.requestSell = MagicMock()

        def ret(callback, req, callback_failure=None, strat=None):
            res = TradeResponse(request=req,
                                side=req.side,
                                price=req.price,
                                volume=req.volume,
                                success=True)
            callback(res)

        s._te.requestBuy.side_effect = ret
        s._te.requestSell.side_effect = ret

        data = [MarketData(type=TickType.TRADE,
                           time=parse_date('1479272400'),
                           price=float(x),
                           volume=float(100),
                           side=Side.BUY) for x in range(10)]

        for x in range(1, 11):
            s.onTrade(data[-x])

        assert s.shorts == [0]
        assert s.longs == [4, 3, 2, 1, 0]
        assert s.short_av == 0
        assert s.long_av == 2

        assert s._portfolio_value == []
        assert s.bought == 0

        s.onTrade(data[5])  # short ticks up

        assert s.shorts == [5]
        assert s.longs == [3, 2, 1, 0, 5]
        assert s.short_av == 5
        assert s.long_av == 2.2

        assert s._portfolio_value[0]
        assert s.bought == 5

        self.s = s

    def test_sma_sell(self):
        self.test_sma_buy()

        from ...lib.enums import TickType, Side
        from ...lib.structs import MarketData
        from ...lib.utils import parse_date

        data = MarketData(type=TickType.TRADE,
                          time=parse_date('1479272400'),
                          price=float(0),
                          volume=float(100),
                          side=Side.BUY)

        s = self.s
        s.onTrade(data)

        assert s.shorts == [0]
        assert s.longs == [2, 1, 0, 5, 0]
        assert s.short_av == 0
        assert s.long_av == 1.6
        assert s.bought == 0
        assert s.profits == -5

    # @patch('matplotlib.pyplot')
    def test_plot(self):
        import matplotlib
        matplotlib.use('agg')
        with patch('matplotlib.pyplot.subplots') as mm1, \
             patch('matplotlib.pyplot.show'), \
             patch('matplotlib.pyplot.show'), \
             patch('matplotlib.pyplot.title'):
            mm1.return_value = (MagicMock(), MagicMock())
            # mm2= MagicMock()

            # for coverage
            self.test_sma_buy()
            self.test_sma_sell()
            self.s.onAnalyze(None)
