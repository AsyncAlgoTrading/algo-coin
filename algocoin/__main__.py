import sys
import tornado
import threading
from .custom_strategies import CustomStrategy
from .lib.strategies.sma_crosses_strategy import SMACrossesStrategy
from .lib.strategies.test_strat import TestStrategy
from .trading import TradingEngine
# from .lib.parser import parse_command_line_config, parse_config
from .lib.parser import parse_command_line_config
from .lib.logging import LOG as log
from .ui.server import ServerApplication


def main(argv: list) -> None:
    config = parse_command_line_config(argv)

    port = 8889
    # config = parse_config(argv)

    # Instantiate trading engine
    #
    # The engine is responsible for managing the different components,
    # including the strategies, the bank/risk engine, and the
    # exchange/backtest engine.
    te = TradingEngine(config)
    application = ServerApplication(te)

    # A sample strategy that impelements the correct interface
    # ts = CustomStrategy(50)
    # ts2 = SMACrossesStrategy(5, 10)
    ts = TestStrategy()
    te.registerStrategy(ts)
    # te.registerStrategy(ts)
    # te.registerStrategy(ts2)

    # for i in [5, 10, 20, 25, 50, 100]:
    #     for j in [10, 20, 25, 75, 100, 150, 200]:
    #         if j > i:
    #             ts = CustomStrategy(i, j)

    #             # Register the strategy with the Trading engine
    #             log.critical("registering %d - %d", i, j)
    #             te.registerStrategy(ts)

    log.critical('Server listening on port: %s', port)
    application.listen(port)
    t = threading.Thread(target=tornado.ioloop.IOLoop.current().start)
    t.daemon = True  # So it terminates on exit
    t.start()

    # Run the live trading engine
    te.run()


if __name__ == '__main__':
    main(sys.argv)
