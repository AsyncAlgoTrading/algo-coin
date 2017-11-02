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
            set_all_trading_types(TradingType.LIVE, config)
        elif general['TradingType'].lower() == 'sandbox':
            set_all_trading_types(TradingType.SANDBOX, config)
        elif general['TradingType'].lower() == 'backtest':
            set_all_trading_types(TradingType.BACKTEST, config)
        else:
            raise ConfigException('Trading type not recognized : %s',
                                  general['TradingType'])
    else:
        raise ConfigException('TradingType unspecified')

    if 'verbose' in general:
        if int(general['verbose']) >= 1:
            set_verbose(int(general['verbose']))

    if 'print' in general:
        if general['print'] == '1':
            config.print = True


def _parse_exchange(exchange, config) -> None:
    if config.type == TradingType.LIVE:
        _parse_live_options(exchange, config)

    elif config.type == TradingType.SANDBOX:
        _parse_sandbox_options(exchange, config)

    elif config.type == TradingType.BACKTEST:
        _parse_backtest_options(exchange, config)

    else:
        ConfigException('No Trading Type specified in config!')


def _parse_strategy(strategy, config) -> None:

    pass


def _parse_risk(risk, config) -> None:
    pass


def _parse_default(default, config) -> None:
    pass


def _parse_args_to_dict(argv: list) -> dict:
    ret = {}
    for item in argv[1:]:
        if '--' not in item:
            log.critical('Argument not recognized: %s', item)
        value = item.split('--')[1]
        if '=' in value:
            # = args
            splits = value.split('=')
            ret[splits[0]] = splits[-1]
        else:
            # single args
            if value.upper() in TradingType.members():
                ret['ttype'] = value
            elif value.upper() == 'VERBOSE':
                ret['verbose'] = True
            elif value.upper() == 'PRINT':
                ret['print'] = True
            else:
                log.critical('Argument not recognized: %s', item)
    return ret


def _parse_live_options(argv, config: TradingEngineConfig) -> None:
    log.critical("WARNING: Live trading. money will be lost ;^)")
    config.exchange_options.exchange_type = \
        str_to_exchange(argv.get('exchange', ''))


def _parse_sandbox_options(argv, config) -> None:
    log.critical("Sandbox trading")
    config.exchange_options.exchange_type = \
        str_to_exchange(argv.get('exchange', ''))


def _parse_backtest_options(argv, config) -> None:
    log.critical("Backtesting")
    config.backtest_options = BacktestConfig()
    config.backtest_options.file = \
        exchange_to_file(str_to_exchange(argv.get('exchange', '')))
    config.exchange_options.exchange_type = \
        str_to_exchange(argv.get('exchange', ''))
    config.risk_options.total_funds = 20000.0


def parse_command_line_config(argv: list) -> TradingEngineConfig:
    # Every engine run requires a static config object
    argv = _parse_args_to_dict(argv)

    if argv.get('config'):
        config = parse_file_config(argv.get('config'))
    else:
        config = TradingEngineConfig()

        if 'live' == argv.get('ttype'):
            # WARNING: Live trading. money will be lost ;^)
            set_all_trading_types(TradingType.LIVE, config)
            _parse_live_options(argv, config)

        elif 'sandbox' == argv.get('ttype'):
            # Trade against sandbox
            _parse_sandbox_options(argv, config)
            set_all_trading_types(TradingType.SANDBOX, config)

        elif 'backtest' == argv.get('ttype'):
            # Backtest against trade data
            set_all_trading_types(TradingType.BACKTEST, config)
            _parse_backtest_options(argv, config)
        else:
            raise ConfigException('Trading Type not specified')

        if argv.get('verbose'):
            set_verbose()

        if argv.get('print'):
            config.print = True

    log.critical("Config : %s", str(config))

    return config


def set_all_trading_types(trading_type: TradingType,
                          config: TradingEngineConfig) -> None:
    config.type = trading_type
    config.exchange_options.trading_type = trading_type
    config.risk_options.trading_type = trading_type
    config.execution_options.trading_type = trading_type
