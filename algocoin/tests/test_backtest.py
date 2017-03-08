class TestBacktest:
    def setup(self):
        from ..lib.config import BacktestConfig
        self.config = BacktestConfig()
        self.config.file = 'test'

        self.test_line = '1479272400,1,100'

    def teardown(self):
        pass
        # teardown() after each test method

    @classmethod
    def setup_class(cls):
        from ..lib.callback import Callback

        class CallbackTester(Callback):
            def __init__(self):
                self._onTrade = False
                self._onReceived = False
                self._onOpen = False
                self._onDone = False
                self._onChange = False
                self._onError = False
                self._onAnalyze = False
                self._onHalt = False
                self._onContinue = False

            def onTrade(self, data):
                self._onTrade = True

            def onReceived(self, data):
                self._onReceived = True

            def onOpen(self, data):
                self._onOpen = True

            def onDone(self, data):
                self._onDone = True

            def onChange(self, data):
                self._onChange = True

            def onError(self, data):
                self._onError = True

            def onAnalyze(self, data):
                self._onAnalyze = True

            def onHalt(self, data):
                self._onHalt = True

            def onContinue(self, data):
                self._onContinue = True

        cls.demo_callback = CallbackTester

    @classmethod
    def teardown_class(cls):
        pass
        # teardown_class() after any methods in this class

    def test_init(self):
        from ..backtest import Backtest
        b = Backtest(self.config)
        assert b
        assert b._file == 'test'

    def test_receive(self):
        from ..backtest import Backtest

        b = Backtest(self.config)
        cb = self.demo_callback()

        b.registerCallback(cb)
        b.receive(self.test_line)
        assert cb._onTrade
