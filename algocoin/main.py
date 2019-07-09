from aat.trading import TradingEngine
from aat.parser import parse_command_line_config
from .ui.server import getHandlers


def main(argv: list) -> None:
    config = parse_command_line_config(argv)

    settings, handlers = getHandlers()

    # Instantiate trading engine
    #
    # The engine is responsible for managing the different components,
    # including the strategies, the bank/risk engine, and the
    # exchange/backtest engine.
    te = TradingEngine(config, ui_handlers=handlers, ui_settings=settings)

    # Run the live trading engine
    te.run()
