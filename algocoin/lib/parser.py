import logging
from .config import TradingEngineConfig, BacktestConfig
from .enums import TradingType
from .logging import LOG as log, \
                         STRAT as slog, \
                         DATA as dlog, \
                         RISK as rlog, \
                         EXEC as exlog, \
                         SLIP as sllog, \
                         TXNS as tlog, \
                         MANUAL as mlog, \
                         ERROR as elog
from .utils import str_to_exchange, exchange_to_file


def parse_command_line_config(argv: list) -> TradingEngineConfig:
    # Every engine run requires a static config object
    config = TradingEngineConfig()
    if 'live' in argv:
        # WARNING: Live trading. money will be lost ;^)
        log.critical("WARNING: Live trading. money will be lost ;^)")
        config.type = TradingType.LIVE
        config.exchange_options.trading_type = TradingType.LIVE
        config.risk_options.trading_type = TradingType.LIVE
        config.execution_options.trading_type = TradingType.LIVE
        config.exchange_options.exchange_type = str_to_exchange(argv)

    elif 'sandbox' in argv:
        # Trade against sandbox
        log.critical("Sandbox trading")
        config.type = TradingType.SANDBOX
        config.exchange_options.trading_type = TradingType.SANDBOX
        config.risk_options.trading_type = TradingType.SANDBOX
        config.execution_options.trading_type = TradingType.SANDBOX
        config.exchange_options.exchange_type = str_to_exchange(argv)

    elif 'backtest' in argv:
        # Backtest against trade data
        log.critical("Backtesting")
        config.type = TradingType.BACKTEST
        config.backtest_options = BacktestConfig()

        config.backtest_options.file = exchange_to_file(str_to_exchange(argv))
        config.exchange_options.trading_type = TradingType.BACKTEST
        config.exchange_options.exchange_type = str_to_exchange(argv)
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
