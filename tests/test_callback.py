class TestCallback:
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

    def test_null_callback(self):
        from callback import NullCallback
        nc = NullCallback()
        assert nc.onMatch(None) == None

    def test_print_callback(self):
        from callback import Print
        pc = Print(onError=False)
        assert pc.onError == False
        assert pc.onMatch('test-print_onMatch') == None
