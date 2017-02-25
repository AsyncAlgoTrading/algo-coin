import logging
import sys
from .custom_strategies import SMACrossesStrategy
from .lib.config import TradingEngineConfig, BacktestConfig
from .lib.enums import TradingType
from .trading import TradingEngine
from .lib.logging import LOG as log, \
                         OTHER as olog, \
                         STRAT as slog, \
                         WARN as wlog, \
                         ERROR as elog, \
                         DATA as dlog, \
                         TXN as tlog, \
                         MANUAL as mlog


def parse_command_line(argv: list):
    # Every engine run requires a static config object
    config = TradingEngineConfig()
    if 'live' in argv:
        # WARNING: Live trading. money will be lost ;^)
        log.critical("WARNING: Live trading. money will be lost ;^)")
        config.type = TradingType.LIVE
        config.exchange_options.trading_type = TradingType.LIVE
        config.risk_options.trading_type = TradingType.LIVE
        config.execution_options.trading_type = TradingType.LIVE

    elif 'sandbox' in argv:
        # Trade against sandbox
        log.info("Sandbox trading")
        config.type = TradingType.SANDBOX
        config.exchange_options.trading_type = TradingType.SANDBOX
        config.risk_options.trading_type = TradingType.SANDBOX
        config.execution_options.trading_type = TradingType.SANDBOX

    elif 'backtest' in argv:
        # Backtest against trade data
        log.info("Backtesting")
        config.type = TradingType.BACKTEST
        config.backtest_options = BacktestConfig()

        # TODO specify exchange data as input
        if 'bitfinex' in argv:
            log.critical('Backtesting against bitfinex data')
            config.backtest_options.file = "./data/exchange/bitfinexUSD.csv"
        elif 'bitstamp' in argv:
            log.critical('Backtesting against bitstamp data')
            config.backtest_options.file = "./data/exchange/bitstampUSD.csv"
        elif 'itbit' in argv:
            log.critical('Backtesting against itbit data')
            config.backtest_options.file = "./data/exchange/itbitUSD.csv"
        elif 'kraken' in argv:
            log.critical('Backtesting against kraken data')
            config.backtest_options.file = "./data/exchange/krakenUSD.csv"
        elif 'hitbtc' in argv:
            log.critical('Backtesting against hitbtc  data')
            config.backtest_options.file = "./data/exchange/hitbtcUSD.csv"
        elif 'lake' in argv:
            log.critical('Backtesting against lake data')
            config.backtest_options.file = "./data/exchange/lakeUSD.csv"
        else:
            log.critical('Backtesting against coinbase data')
            config.backtest_options.file = "./data/exchange/coinbaseUSD.csv"

        config.exchange_options.trading_type = TradingType.BACKTEST
        config.risk_options.trading_type = TradingType.BACKTEST
        config.execution_options.trading_type = TradingType.BACKTEST

        config.risk_options.total_funds = 10000000000.0

        log.critical("Config : %s", config)

    if 'verbose' in argv:
        # Print/log extra info
        # olog.propagate = True
        # slog.propagate = True
        # elog.propagate = True
        # dlog.propagate = False  # too much
        # tlog.propagate = True
        # mlog.propagate = True
        log.setLevel(logging.DEBUG)
        olog.setLevel(logging.DEBUG)
        slog.setLevel(logging.DEBUG)
        wlog.setLevel(logging.DEBUG)
        elog.setLevel(logging.DEBUG)
        dlog.setLevel(logging.DEBUG)
        tlog.setLevel(logging.DEBUG)
        mlog.setLevel(logging.DEBUG)
        log.info('running in verbose mode!')

    if 'print' in argv:
        config.print = True

    return config


def main(argv: list):
    config = parse_command_line(argv)
    # Instantiate trading engine
    #
    # The engine is responsible for managing the different components,
    # including the strategies, the bank/risk engine, and the
    # exchange/backtest engine.
    te = TradingEngine(config)

    # A sample strategy that impelements the correct interface
    ts = SMACrossesStrategy(10, 5)

    # Register the strategy with the Trading engine
    te.registerStrategy(ts)

    # Run the live trading engine
    te.run()

if __name__ == '__main__':
    main(sys.argv)
