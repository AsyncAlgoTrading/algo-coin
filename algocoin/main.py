import tornado
import threading
from .trading import TradingEngine
from .lib.parser import parse_command_line_config
from .lib.logging import LOG as log
from .ui.server import ServerApplication


def main(argv: list) -> None:
    config = parse_command_line_config(argv)

    port = 8889

    # Instantiate trading engine
    #
    # The engine is responsible for managing the different components,
    # including the strategies, the bank/risk engine, and the
    # exchange/backtest engine.

    te = TradingEngine(config)
    application = ServerApplication(te)

    log.critical('Server listening on port: %s', port)
    application.listen(port)
    t = threading.Thread(target=tornado.ioloop.IOLoop.current().start)
    t.daemon = True  # So it terminates on exit
    t.start()

    # Run the live trading engine
    te.run()
