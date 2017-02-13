import datetime
from .enums import Side, \
                   CurrencyType, \
                   OrderType, \
                   OrderSubType, \
                   ExchangeType, \
                   TickType
from .utils import struct


@struct
class MarketData:
    time = datetime.datetime
    volume = float
    price = float
    type = TickType
    currency = CurrencyType


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
    currency = CurrencyType
    order_type = OrderType
    order_sub_type = OrderSubType
    # exchange = ExchangeType


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
