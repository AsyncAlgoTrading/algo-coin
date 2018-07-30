from datetime import datetime


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

    def test_to_dict(self):
        from ..lib.structs import Instrument
        from ..lib.enums import PairType, InstrumentType
        i = Instrument(underlying=PairType.BTCUSD)
        x = i.to_dict()
        print(x)
        assert x == {'type': InstrumentType.PAIR, 'underlying': PairType.BTCUSD}

    def test_MarketData(self):
        from ..lib.structs import MarketData, Instrument
        from ..lib.enums import TickType, Side, PairType
        m = MarketData(time=datetime.now(),
                       volume=1.0,
                       price=1.0,
                       instrument=Instrument(underlying=PairType.BTCUSD),
                       type=TickType.TRADE,
                       side=Side.BUY)
        # TODO no fields yet
        assert m

    def test_TradeRequest(self):
        from ..lib.structs import TradeRequest, Instrument
        from ..lib.enums import Side, OrderType, PairType
        t = TradeRequest(side=Side.BUY,
                         instrument=Instrument(underlying=PairType.BTCUSD),
                         order_type=OrderType.MARKET,
                         volume=1.0,
                         price=1.0)
        assert t
        # side = Side
        # volume = float
        # price = float
        # exchange = ExchangeType
        # currency = CurrencyType
        # order_type = OrderType
        # order_sub_type = OrderSubType

    def test_TradeResponse(self):
        from ..lib.structs import TradeRequest, TradeResponse, TradeResult, Instrument
        from ..lib.enums import Side, OrderType, PairType
        req = TradeRequest(side=Side.BUY,
                           order_type=OrderType.MARKET,
                           instrument=Instrument(underlying=PairType.BTCUSD),
                           volume=1.0,
                           price=1.0)
        t = TradeResponse(request=req,
                          side=Side.BUY,
                          instrument=Instrument(underlying=PairType.BTCUSD),
                          volume=0.0,
                          price=0.0,
                          status=TradeResult.FILLED,
                          order_id='1')
        assert t
        # side = Side
        # volume = float
        # price = float
        # success = bool
