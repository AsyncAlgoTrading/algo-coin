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
        from datetime import datetime
        from utils import parse_date
        gold = datetime(2016, 11, 16, 0, 0)
        date1 = parse_date('1479272400.0')
        date2 = parse_date('2016-11-16T00:00:00.000000Z')
        print(gold)
        print(date1)
        print(date2)
        
        assert gold == date2
        # FIXME need to localize correctly
        assert gold == date1 == date2

    def test_struct_warnings(self):
        from utils import struct

        @struct
        class Test:
            a = int, 5

        t = Test()

        try:
            print(t.a)
            assert False
        except:
            pass
        t.a = 5
        assert t.a == 5
