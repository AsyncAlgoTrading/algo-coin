from configparser import ConfigParser
from .config import TradingEngineConfig, BacktestConfig
from .enums import TradingType
from .exceptions import ConfigException
from .utils import str_to_exchange, exchange_to_file, set_verbose
from .logging import LOG as log


def parse_file_config(filename: str) -> TradingEngineConfig:
    config = TradingEngineConfig()
    c = ConfigParser()
    c.read(filename)

    general = c['general']
    exchange = c['exchange']
    strategy = c['strategy']
    risk = c['risk']
    default = c['DEFAULT']

    _parse_general(general, config)
    _parse_exchange(exchange, config)
    _parse_strategy(strategy, config)
    _parse_risk(risk, config)
    _parse_default(default, config)
    return config


def _parse_general(general, config) -> None:
    if 'TradingType' in general:
        if general['TradingType'].lower() == 'live':
            log.critical("WARNING: Live trading. money will be lost ;^)")
            set_all_trading_types(TradingType.LIVE, config)
        elif general['TradingType'].lower() == 'sandbox':
            log.critical("Sandbox trading")
            set_all_trading_types(TradingType.SANDBOX, config)
        else:
            log.critical("Backtesting")
            set_all_trading_types(TradingType.BACKTEST, config)
    else:
        raise ConfigException('TradingType unspecified')

    if 'verbose' in general:
        if general['verbose'] == '1':
            set_verbose()


def _parse_exchange(exchange, config) -> None:
    pass


def _parse_strategy(strategy, config) -> None:
    pass


def _parse_risk(risk, config) -> None:
    pass


def _parse_default(default, config) -> None:
    pass


def parse_command_line_config(argv: list) -> TradingEngineConfig:
    # Every engine run requires a static config object
    config = TradingEngineConfig()
    if 'live' in argv:
        # WARNING: Live trading. money will be lost ;^)
        log.critical("WARNING: Live trading. money will be lost ;^)")
        set_all_trading_types(TradingType.LIVE, config)
        config.exchange_options.exchange_type = str_to_exchange(argv)

    elif 'sandbox' in argv:
        # Trade against sandbox
        log.critical("Sandbox trading")
        set_all_trading_types(TradingType.SANDBOX, config)
        config.exchange_options.exchange_type = str_to_exchange(argv)

    elif 'backtest' in argv:
        # Backtest against trade data
        log.critical("Backtesting")
        set_all_trading_types(TradingType.BACKTEST, config)
        config.backtest_options = BacktestConfig()
        config.backtest_options.file = exchange_to_file(str_to_exchange(argv))
        config.exchange_options.exchange_type = str_to_exchange(argv)
        config.risk_options.total_funds = 20000.0

    log.critical("Config : %s", str(config))

    if 'verbose' in argv:
        set_verbose()

    if 'print' in argv:
        config.print = True

    return config


def set_all_trading_types(trading_type: TradingType,
                          config: TradingEngineConfig) -> None:
    config.type = trading_type
    config.exchange_options.trading_type = trading_type
    config.risk_options.trading_type = trading_type
    config.execution_options.trading_type = trading_type
