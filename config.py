from utils import config
from enums import TradingType, ExchangeType


@config
class ExchangeConfig:
    type = ExchangeType, ExchangeType.GDAX


@config
class BacktestConfig:
    file = str


@config
class RiskConfig:
    max_drawdown = float, 100.0  # % Max strat drawdown before liquidation
    max_risk = float, 100.0  # % Max to risk on any trade


@config
class ExecutionConfig:
    pass


@config
class TradingEngineConfig:
    type = TradingType, TradingType.SANDBOX
    verbose = bool, False
    exchange_options = ExchangeConfig, ExchangeConfig()
    backtest_options = BacktestConfig, BacktestConfig()
    risk_options = RiskConfig, RiskConfig()
    execution_options = ExecutionConfig, ExecutionConfig()
