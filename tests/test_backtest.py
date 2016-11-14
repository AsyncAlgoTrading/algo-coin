class TestBacktest:
    def setup(self):
        print("TestUM:setup() before each test method")

    def teardown(self):
        print("TestUM:teardown() after each test method")

    @classmethod
    def setup_class(cls):
        print("setup_class() before any methods in this class")

    @classmethod
    def teardown_class(cls):
        print("teardown_class() after any methods in this class")

    def test_numbers_5_6(self):
        print('test_numbers_5_6()  <= actual test code')
        assert 5 * 6 == 30

    def test_strings_b_2(self):
        print('test_strings_b_2()  <= actual test code')
        assert 'b' * 2 == 'bb'
