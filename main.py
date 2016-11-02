from trading import TradingEngine
from strategy import SMACrossesStrategy


def main():
    te = TradingEngine(sandbox=False, verbose=False)

    ts = SMACrossesStrategy(10, 5)

    te.registerStrategy(ts)

    te.run()

if __name__ == '__main__':
    main()
