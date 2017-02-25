import pytz
import os
from datetime import datetime
from .enums import ExchangeType, CurrencyType, OrderType, OrderSubType
from .logging import WARN as log


def create_pair(key, typ, default=None):
    def get(self):
        if hasattr(self, '__' + str(key)):
            return getattr(self, '__' + str(key))
        if default is not None and type(default) == typ:
            return default
        raise TypeError("%s is unset" % key)

    def set(self, val):
        if not isinstance(val, typ) and not type(val) == typ:
            raise TypeError("%s attribute must be set to an instance of %s"
                            % (key, typ))
        setattr(self, '__' + str(key), val)
    return property(get, set)


def config(cls):
    new_cls_dict = {}
    vars = []
    for k, v in cls.__dict__.items():
        if isinstance(v, type):
            v = create_pair(k, v)
            vars.append(k)
        elif isinstance(v, tuple) and \
                isinstance(v[0], type) and \
                isinstance(v[1], v[0]):
            v = create_pair(k, v[0], v[1])
            vars.append(k)
        new_cls_dict[k] = v
    new_cls_dict['__repr__'] = __repr__
    new_cls_dict['_vars'] = vars
    return type(cls)(cls.__name__, cls.__bases__, new_cls_dict)


def __init__(self, **kwargs):
    for item in self._vars:
        if item not in kwargs:
            log.warn('WARNING %s unset!', item)
        else:
            setattr(self, item, kwargs.get(item))

        getattr(self, item)  # make sure all are set.


def __repr__(self):
    # log.warn(str(self.__class__))
    return '<' + ', '.join([x + '-' +
                           str(getattr(self, x, "UNSET"))
                           for x in self._vars]) + '>'


def struct(cls):
    new_cls_dict = {}
    vars = []
    if len(cls.__bases__) > 1:
        raise Exception("Structs only support single inheritance")
    for k, v in cls.__dict__.items():
        if isinstance(v, type):
            v = create_pair(k, v)
            vars.append(k)
        elif isinstance(v, tuple) and \
                isinstance(v[0], type) and \
                isinstance(v[1], v[0]):
            log.warn('WARNING: no defaults in structs')
            v = create_pair(k, v[0], v[1])
            vars.append(k)
            # v = create_pair(k, v[0])

        new_cls_dict[k] = v
    new_cls_dict['__init__'] = __init__
    new_cls_dict['__repr__'] = __repr__
    new_cls_dict['_vars'] = vars
    return type(cls)(cls.__name__, cls.__bases__, new_cls_dict)


def parse_date(indate: str):
    try:
        date = datetime.utcfromtimestamp(float(indate))
        date = pytz.utc.localize(date).astimezone(
            pytz.timezone('EST')).replace(tzinfo=None)
    except ValueError:
        date = datetime.strptime(indate, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date


def ex_type_to_ex(ex: ExchangeType):
    if ex == ExchangeType.GDAX:
        from .exchanges.gdax import GDAXExchange
        return GDAXExchange


def currency_to_string_gdax(cur: CurrencyType):
    if cur == CurrencyType.BTC:
        return 'BTC-USD'


def order_type_to_string_gdax(typ: OrderType):
    if typ == OrderType.LIMIT:
        return 'limit'
    elif typ == OrderType.MARKET:
        return 'market'


def trade_req_to_params_gdax(req):
    p = {}
    p['price'] = str(req.price)
    p['size'] = str(req.volume)
    p['product_id'] = currency_to_string_gdax(req.currency)
    p['type'] = order_type_to_string_gdax(req.order_type)

    if req.order_sub_type == OrderSubType.FILL_OR_KILL:
        p['time_in_force'] = 'FOK'
    elif req.order_sub_type == OrderSubType.POST_ONLY:
        p['post_only'] = '1'
    return p


def get_keys_from_environment(prefix: str):
    key = os.environ[prefix + '_API_KEY']
    secret = os.environ[prefix + '_API_SECRET']
    passphrase = os.environ[prefix + '_API_PASS']
    return key, secret, passphrase
