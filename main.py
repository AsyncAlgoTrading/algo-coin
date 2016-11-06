import sys
from trading import TradingEngine
from custom_strategies import SMACrossesStrategy


def main(argv):
    # Instantiate trading engine
    #
    # The engine is responsible for managing the different components,
    # including the strategies, the bank/risk engine, and the
    # exchange/backtest engine.
    te = TradingEngine(live=True     if 'live'     in argv else False,
                       sandbox=True  if 'sandbox'  in argv else False,
                       backtest=True if 'backtest' in argv else False,
                       verbose=True  if 'verbose'  in argv else False,
                       bt_file="./data/exchange/krakenUSD.csv")

    # A sample strategy that impelements the correct interface
    ts = SMACrossesStrategy(10, 5)

    # Register the strategy with the Trading engine
    te.registerStrategy(ts)

    # Run the live trading engine
    te.run()

if __name__ == '__main__':
    main(sys.argv)
