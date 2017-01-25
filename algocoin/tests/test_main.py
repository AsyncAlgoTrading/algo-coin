from mock import patch


class TestMain:
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

    def test_parse_command_line(self):
        from ..__main__ import parse_command_line
        from ..lib.enums import TradingType

        argv = ['live']
        ret = parse_command_line(argv)
        assert ret.type == TradingType.LIVE

        argv = ['sandbox']
        ret = parse_command_line(argv)
        assert ret.type == TradingType.SANDBOX

        argv = ['backtest']
        ret = parse_command_line(argv)
        assert ret.type == TradingType.BACKTEST

        argv = ['verbose']
        ret = parse_command_line(argv)
        assert ret.verbose

    def test_main(self):
        from ..__main__ import main
        with patch('algocoin.__main__.TradingEngine'), \
                patch('algocoin.__main__.SMACrossesStrategy'):
            main([])
