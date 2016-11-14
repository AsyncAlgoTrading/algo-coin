import sys
from custom_strategies import SMACrossesStrategy
from config import TradingEngineConfig, BacktestConfig
from enums import TradingType
from trading import TradingEngine


def parse_command_line(argv: list):
    config = TradingEngineConfig()
    if 'live' in argv:
        config.type = TradingType.LIVE
    elif 'sandbox' in argv:
        config.type = TradingType.SANDBOX
    elif 'backtest' in argv:
        config.type = TradingType.BACKTEST
        config.backtest_options = BacktestConfig()
        config.backtest_options.file = "./data/exchange/krakenUSD.csv"

    if 'verbose' in argv:
        config.verbose = True

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
