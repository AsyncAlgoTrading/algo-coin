from trading import TradingEngine
from strategy import SMACrossesStrategy


def main():
    te = TradingEngine(sandbox=False, verbose=False)

    ts = SMACrossesStrategy(5, 10)

    te.registerStrategy(ts)

    te.run()

if __name__ == '__main__':
    main()
