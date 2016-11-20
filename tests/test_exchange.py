from mock import patch, MagicMock


class TestExchange:
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

    def test_init(self):
        from config import ExchangeConfig
        from exchange import Exchange

        ec = ExchangeConfig()
        e = Exchange(ec)
        assert e

    def test_receive(self):
        from config import ExchangeConfig
        from exchange import Exchange

        ec = ExchangeConfig()
        e = Exchange(ec)
        assert e

        e.ws = MagicMock()

        with patch('json.loads') as m1:
            for i, val in enumerate(['match',
                                     'received',
                                     'open',
                                     'done',
                                     'change',
                                     'error']):
                m1.return_value = {'type': val, 'sequence': i}
                e._receive()
