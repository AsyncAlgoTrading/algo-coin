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

    def test_RiskRequest(self):
        from ..lib.structs import RiskRequest
        r = RiskRequest()
        assert r
        # side = Side
        # volume = float
        # price = float

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

    def test_RiskResponse(self):
        from ..lib.structs import RiskResponse
        r = RiskResponse()
        assert r
        # side = Side
        # volume = float
        # price = float
        # success = bool

    def test_TradeResponse(self):
        from ..lib.structs import TradeResponse
        t = TradeResponse()
        assert t
        # side = Side
        # volume = float
        # price = float
        # success = bool

    def test_ExecutionReport(self):
        from ..lib.structs import ExecutionReport
        e = ExecutionReport()
        # TODO no fields yet
        assert e
