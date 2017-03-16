import logging
import sys
from .custom_strategies import CustomStrategy
from .lib.strategies.sma_crosses_strategy import SMACrossesStrategy
from .lib.config import TradingEngineConfig, BacktestConfig
from .lib.enums import TradingType
from .trading import TradingEngine
from .lib.logging import LOG as log, \
                         STRAT as slog, \
                         DATA as dlog, \
                         RISK as rlog, \
                         EXEC as exlog, \
                         SLIP as sllog, \
                         TXNS as tlog, \
                         MANUAL as mlog, \
                         ERROR as elog
from .lib.utils import exchange_str_to_exchange, exchange_to_file


def parse_command_line(argv: list) -> TradingEngineConfig:
    # Every engine run requires a static config object
    config = TradingEngineConfig()
    if 'live' in argv:
        # WARNING: Live trading. money will be lost ;^)
        log.critical("WARNING: Live trading. money will be lost ;^)")
        config.type = TradingType.LIVE
        config.exchange_options.trading_type = TradingType.LIVE
        config.risk_options.trading_type = TradingType.LIVE
        config.execution_options.trading_type = TradingType.LIVE
        config.exchange_options.exchange_type = exchange_str_to_exchange(argv)

    elif 'sandbox' in argv:
        # Trade against sandbox
        log.critical("Sandbox trading")
        config.type = TradingType.SANDBOX
        config.exchange_options.trading_type = TradingType.SANDBOX
        config.risk_options.trading_type = TradingType.SANDBOX
        config.execution_options.trading_type = TradingType.SANDBOX
        config.exchange_options.exchange_type = exchange_str_to_exchange(argv)

    elif 'backtest' in argv:
        # Backtest against trade data
        log.critical("Backtesting")
        config.type = TradingType.BACKTEST
        config.backtest_options = BacktestConfig()

        config.backtest_options.file = exchange_to_file(exchange_str_to_exchange(argv))
        config.exchange_options.trading_type = TradingType.BACKTEST
        config.exchange_options.exchange_type = exchange_str_to_exchange(argv)
        config.risk_options.trading_type = TradingType.BACKTEST
        config.execution_options.trading_type = TradingType.BACKTEST
        config.risk_options.total_funds = 20000.0

    log.critical("Config : %s", str(config))

    if 'verbose' in argv:
        # Print/log extra info
        # olog.propagate = True
        # slog.propagate = True
        # elog.propagate = True
        # dlog.propagate = False  # too much
        # tlog.propagate = True
        # mlog.propagate = True
        log.setLevel(logging.DEBUG)
        slog.setLevel(logging.DEBUG)
        dlog.setLevel(logging.DEBUG)
        rlog.setLevel(logging.DEBUG)
        exlog.setLevel(logging.DEBUG)
        sllog.setLevel(logging.DEBUG)
        tlog.setLevel(logging.DEBUG)
        mlog.setLevel(logging.DEBUG)
        elog.setLevel(logging.DEBUG)
        log.info('running in verbose mode!')

    if 'print' in argv:
        config.print = True

    return config


def main(argv: list) -> None:
    config = parse_command_line(argv)
    # Instantiate trading engine
    #
    # The engine is responsible for managing the different components,
    # including the strategies, the bank/risk engine, and the
    # exchange/backtest engine.
    te = TradingEngine(config)

    # A sample strategy that impelements the correct interface
    ts = CustomStrategy(50)
    ts2 = SMACrossesStrategy(5, 10)
    te.registerStrategy(ts)
    te.registerStrategy(ts2)

    # for i in [5, 10, 20, 25, 50, 100]:
    #     for j in [10, 20, 25, 75, 100, 150, 200]:
    #         if j > i:
    #             ts = CustomStrategy(i, j)

    #             # Register the strategy with the Trading engine
    #             log.critical("registering %d - %d", i, j)
    #             te.registerStrategy(ts)

    # Run the live trading engine
    te.run()

if __name__ == '__main__':
    main(sys.argv)
