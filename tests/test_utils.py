class TestUtils:
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

    def test_config(self):
        from utils import config

        @config
        class Test:
            a = int
            b = str, ''

        t = Test()
        t.a = 5

        assert t.a == 5
        assert t.b == ''

        try:
            t.a = ''
            assert False
        except:
            pass

        t.b = 'test'
        assert t.b == 'test'

    def test_struct(self):
        from utils import struct

        @struct
        class Test:
            a = int
            b = str

        t = Test(a=5, b='')

        assert t.a == 5
        assert t.b == ''

    def test_parse_date(self):
        pass
        # date = datetime.fromtimestamp(float(date))
        # date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
