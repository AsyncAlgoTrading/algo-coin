from enums import Side, CurrencyType, OrderType, OrderSubType, ExchangeType
from utils import struct


@struct
class MarketData:
    pass


@struct
class RiskRequest:
    side = Side
    volume = float
    price = float


@struct
class TradeRequest:
    side = Side
    volume = float
    price = float
    exchange = ExchangeType
    currency = CurrencyType
    order_type = OrderType
    order_sub_type = OrderSubType


@struct
class RiskResponse:
    side = Side
    volume = float
    price = float
    success = bool


@struct
class TradeResponse:
    side = Side
    volume = float
    price = float
    success = bool


@struct
class ExecutionReport:
    volume = float
    price = float
