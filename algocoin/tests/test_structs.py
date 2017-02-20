class TestStructs:
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

    def test_MarketData(self):
        from ..lib.structs import MarketData
        m = MarketData()
        # TODO no fields yet
        assert m

    def test_TradeRequest(self):
        from ..lib.structs import TradeRequest
        t = TradeRequest()
        assert t
        # side = Side
        # volume = float
        # price = float
        # exchange = ExchangeType
        # currency = CurrencyType
        # order_type = OrderType
        # order_sub_type = OrderSubType

    def test_TradeResponse(self):
        from ..lib.structs import TradeResponse
        t = TradeResponse()
        assert t
        # side = Side
        # volume = float
        # price = float
        # success = bool
