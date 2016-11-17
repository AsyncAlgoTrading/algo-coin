from mock import patch, MagicMock


class TestCustomStragies:
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
        from custom_strategies import SMACrossesStrategy
        s = SMACrossesStrategy(1, 5)
        assert s

    def test_sma_match(self):
        from custom_strategies import SMACrossesStrategy
        s = SMACrossesStrategy(1, 5)

        data = [{'type': 'match',
                 'time': '1479272400',
                 'price': x,
                 'volume': 100} for x in range(10)]

        for x in range(10):
            s.onMatch(data[x])

        assert s.shorts == [9]
        assert s.longs == [5, 6, 7, 8, 9]

        assert s.short_av == 9
        assert s.long_av == 7

    def test_sma_buy(self):
        from custom_strategies import SMACrossesStrategy
        s = SMACrossesStrategy(1, 5)

        data = [{'type': 'match',
                 'time': '1479272400',
                 'price': x,
                 'volume': 100} for x in range(10)]

        for x in range(1, 11):
            s.onMatch(data[-x])

        assert s.shorts == [0]
        assert s.longs == [4, 3, 2, 1, 0]
        assert s.short_av == 0
        assert s.long_av == 2

        assert s._portfolio_value == []
        assert s.bought == 0

        s.onMatch(data[5])  # short ticks up

        assert s.shorts == [5]
        assert s.longs == [3, 2, 1, 0, 5]
        assert s.short_av == 5
        assert s.long_av == 2.2

        assert s._portfolio_value[0]
        assert s.bought == 5

        self.s = s

    def test_sma_sell(self):
        self.test_sma_buy()
        data = {'type': 'match',
                'time': '1479272400',
                'price': 0,
                'volume': 100}

        s = self.s
        s.onMatch(data)

        assert s.shorts == [0]
        assert s.longs == [2, 1, 0, 5, 0]
        assert s.short_av == 0
        assert s.long_av == 1.6
        assert s.bought == 0
        assert s.profits == -5

    # @patch('matplotlib.pyplot')
    def test_plot(self):
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
