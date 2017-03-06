from .utils import config
from .enums import TradingType, ExchangeType


@config
class ExchangeConfig:
    exchange_type = ExchangeType
    trading_type = TradingType, TradingType.LIVE


@config
class BacktestConfig:
    file = str


@config
class RiskConfig:
    max_drawdown = float, 100.0  # % Max strat drawdown before liquidation
    max_risk = float, 100.0  # % Max to risk on any trade
    total_funds = float, 0.0
    trading_type = TradingType, TradingType.LIVE


@config
class ExecutionConfig:
    trading_type = TradingType, TradingType.LIVE


@config
class TradingEngineConfig:
    type = TradingType, TradingType.SANDBOX
    print = bool, False
    exchange_options = ExchangeConfig, ExchangeConfig()
    backtest_options = BacktestConfig, BacktestConfig()
    risk_options = RiskConfig, RiskConfig()
    execution_options = ExecutionConfig, ExecutionConfig()
