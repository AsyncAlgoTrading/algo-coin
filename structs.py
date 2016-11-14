from enums import Side
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
    pass
